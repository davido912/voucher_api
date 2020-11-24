import wget
import pandas as pd
import logging
from os.path import dirname
from generators.sql_generators import get_copy_commands
from utility_functions import create_path_if_not_exists

log = logging.getLogger(__name__)


def download_and_convert_parquet(url: str, dst_path: str) -> None:
    """
    downloads to a directory and converts output
    """
    log.info(f"RETRIEVING FILE FROM URL: {url}")
    create_path_if_not_exists(dirname(dst_path))
    wget.download(url, out=dst_path, bar=None)
    df = pd.read_parquet(dst_path)
    log.info(f"SAVING DATAFRAME AS CSV IN {dst_path}.csv")
    df.to_csv(dst_path+'.csv', index=False)


def load_to_db(table_xml_path: str) -> None:
    # airflow hooks have some load time to them, so importing this in sync manner
    # avoids redundant errors to logs and pytests
    from airflow.hooks.postgres_hook import PostgresHook
    hook = PostgresHook('postgres_db')
    sql_commands = get_copy_commands(table_xml_path)
    for sql in sql_commands:
        log.info(f"EXECUTING SQL: {sql}")
    hook.run(sql_commands, autocommit=True)


def download_and_load_to_db(url: str,
                            dst_path: str,
                            table_xml_path: str) -> None:
    download_and_convert_parquet(url, dst_path)
    load_to_db(table_xml_path)

