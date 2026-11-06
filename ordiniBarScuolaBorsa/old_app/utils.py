
from psycopg2.extras import RealDictCursor
from .db import get_conn, put_conn

def bar_aperto():
    con = get_conn(); cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT valore FROM impostazioni WHERE chiave='BAR_APERTO'")
        row = cur.fetchone()
        return row and row['valore'] == 'true'
    finally:
        cur.close(); put_conn(con)

def set_bar(aperto: bool):
    con = get_conn(); cur = con.cursor()
    try:
        cur.execute(
            '''
            INSERT INTO impostazioni(chiave, valore)
            VALUES('BAR_APERTO', %s)
            ON CONFLICT(chiave) DO UPDATE SET valore=EXCLUDED.valore
            ''',
            ("true" if aperto else "false",)
        )
        con.commit()
    finally:
        cur.close(); put_conn(con, commit=False)
