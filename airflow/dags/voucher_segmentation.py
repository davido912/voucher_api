
from dag_utils.my_functions import parse_xml, create_path_if_not_exists
from utility_functions import create_path_if_not_exists, remove_dir_content
from os import listdir
from os.path import join, expandvars
from datetime import datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.latest_only_operator import LatestOnlyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from operator_content.S3.remove_from_S3 import remove_prefix_from_S3
from operator_content.S3.awscli_s3_file_operations import move_s3_prefix_awscli
from operator_content.S3.upload_local_s3_snowflake import new_upload_local_s3_snowflake
from operator_content.mysql_functions.download_query import get_and_split_mysql_results


default_args = {
    'retries': 2,
    'description': 'Voucher Selection pipeline - imports historical voucher data to PostgresDB + modelling',
    'start_date': datetime(2018, 3, 7),
    'catchup': False,
}

# set temp output in environment variable
TEMP_DIR = create_path_if_not_exists((expandvars('$AIRFLOW_TEMP_OUTPUT'), 'voucher_selection'))

dag = DAG(dag_id='voucher_selection',
          schedule_interval=None,
          default_args=default_args)


clean_local = PythonOperator(task_id='clean_local',
                             dag=dag,
                             python_callable=remove_dir_content,
                             op_args=[TEMP_DIR])



backup = PythonOperator(task_id='backup',
                        dag=dag,
                        python_callable=move_s3_prefix_awscli,
                        op_args=[p.S3_BUCKET_MAIN,
                                 p.S3_BUCKET_BACKUPS,
                                 S3_KEY_PREFIX,
                                 join(S3_KEY_PREFIX, S3_KEY_PREFIX + '_' + '{{ ts_nodash }}')
                                 ])

for sql_file_path in [join(SOURCE_QUERIES_DIR, file) for file in listdir(SOURCE_QUERIES_DIR)]:
    base_file_name = Path(sql_file_path).stem
    query_result_dir_path = join(IP_LOCAL_TEMP_DIR, base_file_name)
    query_result_temp_file = join(query_result_dir_path, base_file_name)
    import_files = PythonOperator(task_id='import_%s' % base_file_name,
                                  dag=dag,
                                  python_callable=get_and_split_mysql_results,
                                  op_args=[AURORA_DEU_CONN_ID,
                                           sql_file_path,
                                           query_result_temp_file
                                           ])

    upload_local_to_snowflake = PythonOperator(task_id='load_%s' % base_file_name,
                                               dag=dag,
                                               python_callable=new_upload_local_s3_snowflake,
                                               op_args=[
                                                   S3_CONN_ID,
                                                   query_result_dir_path,
                                                   p.S3_BUCKET_MAIN,
                                                   join(S3_KEY_PREFIX, base_file_name),  # s3 key prefix
                                               ],
                                               op_kwargs={
                                                   'pipeline_metadata': pipeline_metadata,
                                                   'table_metadata_path': join(IP_XML_DIR,
                                                                               base_file_name + ".xml"),
                                                   'file_prefix': base_file_name,
                                               }
                                               )
    clean_s3 >> import_files >> upload_local_to_snowflake >> trigger >> backup
