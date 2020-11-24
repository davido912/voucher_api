from pathlib import Path
import logging
import shutil
from os.path import expandvars
import xml.etree.ElementTree as ET


log = logging.getLogger(__name__)


def parse_xml(path: str) -> ET.Element:
    tree = ET.parse(path)
    root = tree.getroot()
    return root


def directory_scope_limit(func):
    """
    prevents creationg of directories outside of temp to isolate processes
    """
    def wrapped(path):
        if expandvars('$AIRFLOW_TEMP_OUTPUT') not in path:
            raise ValueError(
                f"{func} IS ONLY ALLOWED TO EXECUTE OPERATIONS OUTSIDE OF {expandvars('$AIRFLOW_TEMP_OUTPUT')}")
        func(path=path)
    return wrapped


@directory_scope_limit
def create_path_if_not_exists(path: str) -> str:
    """ This functions creates directory path if it doesn't exist
    :param path: Path to create
    :type path: str
    :return: The path that was created
    :rtype: string
    """
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


# test, what if nothign to remove
@directory_scope_limit
def remove_dir_content(path: str) -> None:
    log.info(f"REMOVING PATH {path} AND ALL OF ITS SUBDIRECTORIES")
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        log.info(f"PATH {path} DOES NOT EXIST")

