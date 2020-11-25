from utility_functions import remove_dir_content, create_path_if_not_exists
from voucher_importer_functions import download_and_load_to_db
from os.path import join, expandvars
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'description': 'Voucher Selection pipeline - imports historical voucher data to PostgresDB + modelling',
    'start_date': days_ago(2),
    'catchup': False,
}

# set temp output in environment variable
TEMP_DIR = join(expandvars('$AIRFLOW_TEMP_OUTPUT'), 'voucher_selection')
create_path_if_not_exists(TEMP_DIR)
OUTPUT_FNAME = "data.parquet.gzip"
TABLE_XML = join(expandvars('$PIPELINE_DIR'), 'voucher', 'table_metadata', 'voucher_payment_hist.xml')
MODELLING_DIR = join(expandvars('$AIRFLOW_HOME'), 'pipeline', 'voucher', 'modelling')
DOWNLOAD_URL = "https://dh-data-chef-hiring-test.s3.eu-central-1.amazonaws.com/data-eng/voucher-selector/data.parquet.gzip"
CUR_DATE = expandvars('$CUR_DATE')

with open(join(MODELLING_DIR, 'voucher_segmentation.sql'), 'r') as sql_file:
    voucher_segmentation_sql = sql_file.read()

with open(join(MODELLING_DIR, 'segment_rules.sql'), 'r') as sql_file:
    segment_rules_sql = sql_file.read()

dag = DAG(dag_id='voucher_selection',
          schedule_interval=None,
          default_args=default_args)

clean_local = PythonOperator(task_id='clean_local',
                             dag=dag,
                             python_callable=remove_dir_content,
                             op_args=[TEMP_DIR])

extract_and_load = PythonOperator(task_id='extract_and_load',
                                  dag=dag,
                                  python_callable=download_and_load_to_db,
                                  op_args=[DOWNLOAD_URL,
                                           join(TEMP_DIR, OUTPUT_FNAME),
                                           TABLE_XML])

segment_rules_modelling = PostgresOperator(task_id='segment_rules_modelling',
                                           dag=dag,
                                           postgres_conn_id='postgres_db',
                                           sql=segment_rules_sql)

voucher_segmentation_modelling = PostgresOperator(task_id='voucher_segmentation_modelling',
                                                  dag=dag,
                                                  postgres_conn_id='postgres_db',
                                                  parameters=(CUR_DATE,),
                                                  sql=voucher_segmentation_sql)

clean_local >> extract_and_load >> segment_rules_modelling >> voucher_segmentation_modelling
