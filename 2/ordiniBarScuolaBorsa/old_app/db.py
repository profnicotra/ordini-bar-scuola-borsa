
import os
from psycopg2.pool import SimpleConnectionPool

PGHOST = os.getenv('PGHOST', 'localhost')
PGPORT = os.getenv('PGPORT', '5432')
PGDATABASE = os.getenv('PGDATABASE', 'bar_db')
PGUSER = os.getenv('PGUSER', 'bar_user')
PGPASSWORD = os.getenv('PGPASSWORD', 'bar_pwd')
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DSN = DATABASE_URL
else:
    DSN = f"host={PGHOST} port={PGPORT} dbname={PGDATABASE} user={PGUSER} password={PGPASSWORD}"

POOL = SimpleConnectionPool(1, 10, dsn=DSN)

def get_conn():
    con = POOL.getconn()
    con.autocommit = False
    return con

def put_conn(con, commit=False):
    try:
        if commit:
            con.commit()
        else:
            con.rollback()
    finally:
        POOL.putconn(con)
