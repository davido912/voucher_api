from pathlib import Path
import logging
import shutil
from os.path import expandvars
import wget
import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

log = logging.getLogger(__name__)


# test
def create_path_if_not_exists(path: str):
    """ This functions creates directory path if it doesn't exist
    :param path: Path to create
    :type path: str
    :return: The path that was created
    :rtype: string
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


# test
def remove_dir_content(path: str):
    log.info(f"REMOVING PATH {path} AND ALL OF ITS SUBDIRECTORIES")
    if path not in expandvars('$AIRFLOW_TEMP_OUTPUT'):
        raise ValueError(
            f"remove_dir_content IS ONLY ALLOWED TO REMOVE FILES INSIDE OF {expandvars('$AIRFLOW_TEMP_OUTPUT')}")
    shutil.rmtree(path)


def download_and_load_parquet_data(url: str, dst_path: str):
    log.info(f"RETRIEVING FILE FROM URL: {url}")
    wget.download(url, out=dst_path)
    df = pd.read_parquet(dst_path)
    log.info(f"SAVING DATAFRAME AS CSV IN {dst_path}.csv")
    df.to_csv(f"{dst_path}.csv", index=False)

# hook = PostgresHook(conn_id='postgres')

def load_to_db():
    # sql_commands
#     execute
    pass
