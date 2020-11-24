CREATE SCHEMA IF NOT EXISTS model_staging;
DROP TABLE IF EXISTS model_staging.segment_rules;

CREATE TABLE IF NOT EXISTS model_staging.segment_rules
(
    segment_type VARCHAR(30),
    segment_name VARCHAR(30),
    lower_floor  INT,
    upper_floor  INT
);

INSERT INTO model_staging.segment_rules VALUES ('frequent_segment', '1-4', 1, 4),
                                               ('frequent_segment', '5-13',5, 13),
                                               ('frequent_segment', '14-37',14, 37),
                                               ('recency_segment', '30-60',30, 60),
                                               ('recency_segment', '61-90',61, 90),
                                               ('recency_segment', '91-120',91, 120),
                                               ('recency_segment', '121-180',121, 180),
                                               ('recency_segment', '180+',180, null);

