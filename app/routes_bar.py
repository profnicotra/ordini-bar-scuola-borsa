
from bottle import redirect
from .utils import set_bar, bar_aperto
from .db import get_conn, put_conn
from . import app

@app.post('/toggle')
def toggle():
    set_bar(not bar_aperto())
    return redirect('/display')

@app.post('/stato/<oid:int>/<nuovo>')
def cambia_stato(oid, nuovo):
    con = get_conn(); cur = con.cursor()
    try:
        cur.execute('UPDATE ordini SET stato=%s WHERE id=%s', (nuovo, oid))
        con.commit()
    finally:
        cur.close(); put_conn(con, commit=False)
    return redirect('/display')
