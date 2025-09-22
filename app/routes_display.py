
from bottle import template
from psycopg2.extras import RealDictCursor
from .db import get_conn, put_conn
from .utils import bar_aperto
from . import app

@app.get('/grazie')
def grazie():
    html = '<div class="card"><div class="title">Ordine inviato!</div><p>Grazie, la sala bar ha ricevuto la comanda.</p><a href="/" class="btn" style="margin-top:8px;display:inline-block">Nuovo ordine</a></div>'
    return template('base', title='Grazie', refresh=3, content=html)

@app.get('/display')
@app.get('/display/<stato>')
def display(stato=None):
    con = get_conn(); cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        if stato:
            cur.execute('''
                SELECT o.id, o.stato, o.creato_il, p.nome AS posizione
                FROM ordini o JOIN posizioni p ON p.id=o.posizione_id
                WHERE o.stato=%s ORDER BY o.creato_il
            ''', (stato,))
        else:
            cur.execute('''
                SELECT o.id, o.stato, o.creato_il, p.nome AS posizione
                FROM ordini o JOIN posizioni p ON p.id=o.posizione_id
                ORDER BY CASE o.stato WHEN 'NUOVO' THEN 0 WHEN 'IN_PREPARAZIONE' THEN 1 WHEN 'PRONTO' THEN 2 WHEN 'CONSEGNATO' THEN 3 WHEN 'ANNULLATO' THEN 4 ELSE 5 END, o.creato_il
            ''')
        ords = cur.fetchall()
        result = []
        for o in ords:
            cur2 = con.cursor(cursor_factory=RealDictCursor)
            cur2.execute('''
                SELECT r.quantita, r.nota, pr.nome AS prodotto
                FROM ordine_righe r JOIN prodotti pr ON pr.id=r.prodotto_id
                WHERE r.ordine_id=%s
            ''', (o['id'],))
            righe = cur2.fetchall(); cur2.close()
            result.append({
                'id': o['id'], 'stato': o['stato'], 'creato_il': o['creato_il'],
                'posizione': o['posizione'], 'righe': righe
            })
        return template('display', ordini=result, aperto=bar_aperto())
    finally:
        cur.close(); put_conn(con)
