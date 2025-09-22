
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
        return template('form', prodotti=prodotti, posizioni=posizioni, aperto=bar_aperto(), iniziali=2)
    finally:
        cur.close(); put_conn(con)

@app.post('/ordina')
def ordina():
    if not bar_aperto():
        return template('base', title='Bar chiuso', refresh=None, content='<div class="card"><b>Bar chiuso</b></div>')

    f = request.forms
    posizione_id = int(f.get('posizione_id'))
    creato_da = f.get('creato_da') or ''

    righe = []
    for k in f:
        if k.startswith('prodotto_id_'):
            idx = k.split('_')[-1]
            try:
                prod_id = int(f.get(f'prodotto_id_{idx}'))
                q = int(f.get(f'quantita_{idx}', '1'))
                nota = (f.get(f'nota_{idx}', '') or '').strip() or None
            except (TypeError, ValueError):
                continue
            if q > 0:
                righe.append((prod_id, q, nota))

    if not righe:
        return template('base', title='Errore', refresh=None, content='<div class="card"><b>Nessun prodotto selezionato.</b></div>')

    con = get_conn(); cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        totale = Decimal('0.00')
        for prod_id, q, _ in righe:
            cur.execute('SELECT prezzo_euro FROM prodotti WHERE id=%s', (prod_id,))
            row = cur.fetchone()
            prezzo = row['prezzo_euro'] or Decimal('0.00')
            totale += (prezzo * q)

        cur.execute('INSERT INTO ordini (posizione_id, creato_da, totale_euro) VALUES (%s,%s,%s) RETURNING id',
                    (posizione_id, creato_da, totale.quantize(Decimal('0.01'))))
        ordine_id = cur.fetchone()['id']

        for prod_id, q, nota in righe:
            cur.execute('SELECT prezzo_euro FROM prodotti WHERE id=%s', (prod_id,))
            row = cur.fetchone()
            cur.execute('''
                INSERT INTO ordine_righe (ordine_id, prodotto_id, quantita, nota, prezzo_euro_unit)
                VALUES (%s,%s,%s,%s,%s)
            ''', (ordine_id, prod_id, q, nota, row['prezzo_euro']))

        con.commit()
    finally:
        cur.close(); put_conn(con, commit=False)

    return redirect('/grazie')
