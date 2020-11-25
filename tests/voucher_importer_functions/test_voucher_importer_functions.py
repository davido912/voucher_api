import pytest
from os.path import expandvars, join
from voucher_importer_functions import download_and_convert_parquet, load_to_db
from urllib.error import URLError
from unittest.mock import MagicMock
from psycopg2.errors import DuplicateSchema
from airflow.hooks.postgres_hook import PostgresHook

TEST_DIR = join(expandvars('$AIRFLOW_TEMP_OUTPUT'), 'testing')


@pytest.mark.parametrize("url,dst_path",
                         [
                             ("https://www.url.does.not.exist", TEST_DIR)
                         ]
                         )
def test_download_and_convert_parquet_params(url: str, dst_path: str) -> None:
    with pytest.raises(URLError):
        download_and_convert_parquet(url, dst_path)


@pytest.fixture
def cleanUp():
    yield
    hook = PostgresHook('postgres_db')
    hook.run("DROP SCHEMA test_schema;")


# using a mock because get_copy_commands is tested.
# this tests the SQL execution to the database and that the schema was indeed created
# therefore, if the DuplicateSchema error was raised then the schema was created
def test_load_to_db(mocker, cleanUp):
    mock_copy_commands = MagicMock(return_value=['CREATE SCHEMA test_schema;'])
    mocker.patch("voucher_importer_functions.get_copy_commands", mock_copy_commands)
    load_to_db('mock')
    hook = PostgresHook('postgres_db')
    with pytest.raises(DuplicateSchema):
        hook.run('CREATE SCHEMA test_schema;')



