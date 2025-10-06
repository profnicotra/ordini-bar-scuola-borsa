
from bottle import template, request, redirect
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from .db import get_conn, put_conn
from .utils import bar_aperto
from . import app

@app.get('/')
def form():
    con = get_conn(); cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('SELECT id, nome, prezzo_euro FROM prodotti WHERE attivo=true ORDER BY nome')
        prodotti = cur.fetchall()
        cur.execute('SELECT id, nome FROM posizioni ORDER BY nome')
        posizioni = cur.fetchall()
        #return template('form', prodotti=prodotti, posizioni=posizioni, aperto=bar_aperto(), iniziali=2)
    finally:
        #cur.close(); put_conn(con)

@app.post('/ordina')
def ordina():
    if not bar_aperto():
        return template('base', title='Bar chiuso', refresh=None, content='<div class="card"><b>Bar chiuso</b></div>')



    return redirect('/grazie')
