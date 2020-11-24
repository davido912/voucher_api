import pytest
from urllib.error import URLError
from os.path import expandvars
from airflow_do.plugins.voucher_importer_functions import download_and_convert_parquet

TEMP_DIR = expandvars('$AIRFLOW_TEMP_OUTPUT')
# download_and_convert_parquet, TODO: check more execution tests
@pytest.mark.parametrize("url,dst_path",
                         [
                             ("https://www.url.does.not.exist", TEMP_DIR)
                         ]
                         )
def test_download_and_convert_parquet_params(url, dst_path):
    with pytest.raises(URLError):
        download_and_convert_parquet(url, dst_path)
