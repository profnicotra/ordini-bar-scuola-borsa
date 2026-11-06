
import os
from .db import get_conn, put_conn

def _read_sql(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def _exec_multi(con, sql_text):
    cur = con.cursor()
    try:
        for stmt in sql_text.split(';'):
            s = stmt.strip()
            if s:
                cur.execute(s + ';')
        con.commit()
    finally:
        cur.close()

def init_db():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    schema = _read_sql(os.path.join(root, 'schema.sql'))
    seed   = _read_sql(os.path.join(root, 'seed.sql'))
    con = get_conn()
    try:
        _exec_multi(con, schema)
        _exec_multi(con, seed)
    finally:
        put_conn(con)
