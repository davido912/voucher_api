from utility_functions import parse_xml
from typing import List
from os.path import join
import xml.etree.ElementTree as ET


def drop_table_if_exists(schema: str, table: str) -> str:
    return f"DROP TABLE IF EXISTS {schema}.{table};"


def create_schema(schema: str) -> str:
    return f"CREATE SCHEMA IF NOT EXISTS {schema};"


def create_table(schema: str, table_name: str, columns_metadata: List[ET.Element]) -> str:
    """
    This function returns a custom CREATE TABLE SQL string according to an XML containing table metadata.
    """

    create_table_sql = "CREATE TABLE IF NOT EXISTS {schema}.{table_name}({columns});"
    columns = []
    for column_md in columns_metadata:
        col = f"{column_md.get('name')} {column_md.get('type')}"
        if column_md.get('length'):
            col += f"({column_md.get('length')})"
        columns.append(col)

    return create_table_sql.format(schema=schema,
                                   table_name=table_name,
                                   columns=','.join(columns))


def copy_query(schema: str,
               table_name: str,
               columns_metadata: List[ET.Element],
               file_path: str,
               delimiter: str,
               header: bool) -> str:
    return """COPY {schema}.{table_name} ({columns}) 
    FROM '{file_path}'
    DELIMITER '{delimiter}'
    CSV {header}
    """.format(schema=schema,
               table_name=table_name,
               columns=','.join([col.get('name') for col in columns_metadata]),
               file_path=file_path,
               delimiter=delimiter,
               header='HEADER' if header else None
               )


def get_copy_commands(table_xml_path: str) -> List[str]:
    table_metadata = parse_xml(table_xml_path)
    table_schema = table_metadata.attrib.get('schema')
    table_name = table_metadata.attrib.get('name')
    columns = [md for md in table_metadata.find('columns')]
    file_path = join(table_metadata.find('source').get('path'),
                     table_metadata.find('source').get('file'))
    delimiter = table_metadata.find('source').get('delimiter')
    header = table_metadata.find('source').get('header')

    return [
        drop_table_if_exists(schema=table_schema,
                             table=table_name),
        create_schema(schema=table_schema),
        create_table(schema=table_schema,
                     table_name=table_name,
                     columns_metadata=columns),
        copy_query(schema=table_schema,
                   table_name=table_name,
                   columns_metadata=columns,
                   file_path=file_path,
                   delimiter=delimiter,
                   header=header)
    ]







