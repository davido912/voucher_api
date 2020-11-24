import pytest
from os.path import expandvars, join
from voucher_importer_functions import download_and_convert_parquet
from urllib.error import URLError

TEST_DIR = join(expandvars('$AIRFLOW_TEMP_OUTPUT'), 'testing')
# download_and_convert_parquet, TODO: check more execution tests
@pytest.mark.parametrize("url,dst_path",
                         [
                             ("https://www.url.does.not.exist", TEST_DIR)
                         ]
                         )
def test_download_and_convert_parquet_params(url, dst_path):
    with pytest.raises(URLError):
        download_and_convert_parquet(url, dst_path)
