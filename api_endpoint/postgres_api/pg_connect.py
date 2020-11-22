import psycopg2
import psycopg2.extras
from contextlib import closing



database = 'airflow'
user = 'airflow'
password = 'airflow'
host = 'localhost'


class PgHook:
    def __init__(self, database, user, password, host):
        self.database = database
        self.user = user
        self.password = password
        self.host = host

    def get_conn(self):
        return psycopg2.connect(database=self.database,
                                user=self.user,
                                password=self.password,
                                host=self.host)

    def execute_query(self, query):
        with closing(self.get_conn().cursor(cursor_factory = psycopg2.extras.DictCursor)) as cur:
            cur.execute(query)
            # print(cur.description)
            return cur.fetchall()


if __name__ =='__main__':
    hook = PgHook(database, user, password, host)
    data = hook.execute_query("""select * from model_staging.segments where segment_type='recency_segment' and
                                           minimum <= 190 and (maximum >= 190 or maximum is null)""")
    print(data[0]['voucher_amount'])
