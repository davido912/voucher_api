import psycopg2
import psycopg2.extras
from contextlib import closing
from typing import List


class PgHook:
    """
    This hook is used externally to Airflow to connect the API to the Postgres Database containing voucher related
    data.
    :param database: database name containing the relevant schemas & tables
    :type database: str
    :param user: username to log in the database
    :type user: str
    :param password: password relevant to the user to log in the database
    :type password: str
    :param host: the endpoint to connect to the database (e.g. localhost)
    :type host: str
    :param port: port exposed by postgres to connect through (default 5432)
    :type port: int
    """

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_conn(self):
        """
        This method returns a connection object for postgres.
        """
        return psycopg2.connect(database=self.database,
                                user=self.user,
                                password=self.password,
                                host=self.host,
                                port=self.port)

    def execute_query(self, query: str) -> List[List[psycopg2.extras.DictRow]]:
        """
        This method executes a query and fetches all of the results in the query (think about yielding)
        :return: A list of lists, where each list contains a psycopg2 DictRow object which allows
                to key -> value retrieve values from it
        :rtype: List[List[psycopg2.extras.DictRow]
        """
        with closing(self.get_conn().cursor(cursor_factory=psycopg2.extras.DictCursor)) as cur:
            cur.execute(query)
            return cur.fetchall()
