CREATE SCHEMA IF NOT EXISTS model_production;
DROP TABLE IF EXISTS model_production.voucher_segmentation;
CREATE TABLE IF NOT EXISTS model_production.voucher_segmentation AS(
WITH base AS (
    SELECT %s AS cur_date,
           *
    FROM raw.voucher_payment_hist
    WHERE lower(country_code) = 'peru'
      AND total_orders IS NOT NULL
      AND voucher_amount IS NOT NULL
),
     date_diff_ts AS (
         SELECT *,
                (cur_date::DATE - last_order_ts::DATE) AS datediff_last_order
         FROM base
     ),
     invalid_entries AS (
         SELECT *,
                CASE
--      when customer did not make any orders but actually entry contains order date, the entry is invalid
                    WHEN total_orders = 0 AND (last_order_ts IS NOT NULL OR first_order_ts IS NOT NULL) THEN TRUE
--      when last order happened before first order, entry is invalid
                    WHEN last_order_ts < first_order_ts THEN TRUE
                    ELSE FALSE
                    END AS invalid
         FROM date_diff_ts
     ),
     segments AS (
         SELECT *,
                CASE
                    WHEN total_orders BETWEEN 1 AND 4 THEN '1-4'
                    WHEN total_orders BETWEEN 5 AND 13 THEN '5-13'
                    WHEN total_orders BETWEEN 14 AND 37 THEN '14-37'
                    WHEN total_orders > 37 THEN 'out_of_range'
                    END AS frequent_segment,
                CASE
                    WHEN datediff_last_order BETWEEN 30 AND 60 THEN '30-60'
                    WHEN datediff_last_order BETWEEN 61 AND 90 THEN '61-90'
                    WHEN datediff_last_order BETWEEN 91 AND 120 THEN '91-120'
                    WHEN datediff_last_order BETWEEN 121 AND 180 THEN '121-180'
                    WHEN datediff_last_order > 180 THEN '180+'
                    END AS recency_segment

         FROM invalid_entries
         WHERE NOT invalid
     ),
     most_used_voucher_values_frequent AS (
         SELECT 'frequent_segment' AS segment_type,
                frequent_segment,
                voucher_amount,
                count(*)           AS count_occurrences
         FROM segments
         GROUP BY 1, 2, 3
     ),
     most_used_voucher_values_frequent_partition AS (
         SELECT *,
                ROW_NUMBER() OVER (PARTITION BY frequent_segment ORDER BY count_occurrences DESC) AS row_num
         FROM most_used_voucher_values_frequent
     ),
     most_used_voucher_values_recency AS (
         SELECT 'recency_segment' AS segment_type,
                recency_segment,
                voucher_amount,
                count(*)          AS count_occurrences
         FROM segments
         GROUP BY 1, 2, 3
     ),
     most_used_voucher_values_recency_partition AS (
         SELECT *,
                ROW_NUMBER() OVER (PARTITION BY recency_segment ORDER BY count_occurrences DESC) AS row_num
         FROM most_used_voucher_values_recency
     ),
     unioned_dataset AS (
         SELECT segment_type,
                frequent_segment AS segment_name,
                voucher_amount,
                count_occurrences
         FROM most_used_voucher_values_frequent_partition
         WHERE row_num = 1
         UNION ALL
         SELECT segment_type,
                recency_segment AS segment_name,
                voucher_amount,
                count_occurrences
         FROM most_used_voucher_values_recency_partition
         WHERE row_num = 1
     )

SELECT t1.segment_type,
       t1.segment_name,
       lower_floor,
       upper_floor,
       voucher_amount
FROM unioned_dataset t1
         LEFT JOIN model_staging.segment_rules t2
                   ON t1.segment_type = t2.segment_type AND t1.segment_name = t2.segment_name);