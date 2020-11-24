import re
from unittest.mock import MagicMock
from airflow_do.plugins.generators.sql_generators import (drop_table_if_exists, create_schema,
                                                          create_table, copy_query, get_copy_commands)
from typing import List

test_schema = "test_schema"
test_table = "test_table"
test_file_path = "/test_path"

# expected output sql queries
expected_drop_table = "DROP TABLE IF EXISTS test_schema.test_table;"
expected_create_schema = "CREATE SCHEMA IF NOT EXISTS test_schema;"
expected_create_table = "CREATE TABLE IF NOT EXISTS test_schema.test_table(column1 VARCHAR,column2 VARCHAR(50));"
expected_copy_query = "COPY test_schema.test_table (column1,column2) FROM '/test_path' DELIMITER ',' CSV HEADER"


def test_drop_table_if_exists_return():
    assert expected_drop_table == drop_table_if_exists(test_schema, test_table)


def test_create_schema_return():
    assert expected_create_schema == create_schema(test_schema)


def mock_xml_columns() -> List[MagicMock]:

    def _side_effect(param, column, length=None):
        if param == 'length' and length:
            return length
        elif param == 'type':
            return 'VARCHAR'
        elif param == 'name':
            return column

    column_md_no_len_mock = MagicMock()
    column_md_no_len_mock.get = MagicMock(side_effect=lambda x: _side_effect(x, 'column1'))
    column_md_mock = MagicMock()
    column_md_mock.get = MagicMock(side_effect=lambda x: _side_effect(x, 'column2', 50))
    return [column_md_no_len_mock, column_md_mock]


def test_create_table():
    columns = mock_xml_columns()
    result = create_table(test_schema, test_table, columns)
    assert expected_create_table == result


def test_copy_query():
    columns = mock_xml_columns()
    res = copy_query(test_schema, test_table, columns, test_file_path, ',', True)
    # copy_query returns the SQL with whitespaces, so removing all whitespaces to compare outputs
    assert re.sub("\s*", "", expected_copy_query) == re.sub("\s*", "", res)


def test_get_copy_commands():
    results = get_copy_commands('./test_xml_metadata.xml')
    expected = [expected_drop_table, expected_create_schema,
                expected_create_table,
                expected_copy_query
                ]
    for result, expected in zip(results, expected):
        assert re.sub("\s*", "", result) == re.sub("\s*", "", expected)

