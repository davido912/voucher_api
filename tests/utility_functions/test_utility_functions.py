import pytest
from unittest.mock import MagicMock
from utility_functions import remove_dir_content, \
    create_path_if_not_exists
from os.path import expandvars, dirname, join
from os import listdir


TEMP_DIR = expandvars('$AIRFLOW_TEMP_OUTPUT')
TEST_DIR = join(TEMP_DIR, 'testing')


# this fixture tears down the created environment after unittests so no testing directly is left behind
@pytest.fixture
def cleanUp():
    yield
    remove_dir_content(TEST_DIR)


# create_path_if_not_exists
def test_create_path_outside_scope(mocker):
    mock = MagicMock()
    mocker.patch("plugins.utility_functions.Path", mock)
    with pytest.raises(ValueError):
        create_path_if_not_exists(dirname(TEMP_DIR))
    mock.assert_not_called()


# running twice to ensure no error is raised
@pytest.mark.parametrize("path",
                         [
                             TEST_DIR,
                             TEST_DIR]
                         )
def test_create_path_if_not_exists(path, cleanUp):
    create_path_if_not_exists(path)
    assert path.split('/')[-1] in listdir(TEMP_DIR)  # splitting the path to take just the directory


# remove_dir_content, mock is for not actually deleting the folders but checking
# if paths outside of temp folder raise an error
def test_remove_dir_content_scope(mocker):
    mock = MagicMock()
    mocker.patch("plugins.utility_functions.shutil.rmtree", mock)
    with pytest.raises(ValueError):
        remove_dir_content(dirname(TEMP_DIR))
    mock.assert_not_called()


# test that FileNotFoundError is raised when path does not exist
def test_remove_dir_content_path():
    with pytest.raises(FileNotFoundError):
        remove_dir_content(join(TEMP_DIR, "path_not_exists"))


def test_remove_dir_content(mocker):
    mock = MagicMock()
    mocker.patch("plugins.utility_functions.shutil.rmtree", mock)
    remove_dir_content(TEMP_DIR)
    mock.assert_called_once()


