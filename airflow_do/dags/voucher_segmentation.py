from utility_functions import remove_dir_content
from voucher_importer_functions import download_and_load_to_db
from os.path import join, expandvars
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'description': 'Voucher Selection pipeline - imports historical voucher data to PostgresDB + modelling',
    'start_date': datetime(2018, 3, 7),
    'catchup': False,
}

# set temp output in environment variable
TEMP_DIR = join(expandvars('$AIRFLOW_TEMP_OUTPUT'), 'voucher_selection')
OUTPUT_FNAME = "data.parquet.gzip"
TABLE_XML = join(expandvars('$PIPELINE_DIR'), 'voucher', 'table_metadata', 'voucher_payment_hist.xml')
DOWNLOAD_URL = "https://dh-data-chef-hiring-test.s3.eu-central-1.amazonaws.com/data-eng/voucher-selector/data.parquet.gzip"

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

clean_local >> extract_and_load
