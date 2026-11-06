# app_pg.py
# MVP super-semplice per comande bar scolastico – versione PostgreSQL
# Stack: Bottle (micro web framework) + psycopg2 (senza ORM) + HTML minimale
# Avvio:
#   pip install bottle psycopg2-binary
#   (imposta le variabili PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD)
#   python app_pg.py

from bottle import Bottle, run, template, request, redirect, static_file
import os
from decimal import Decimal
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool

APP = Bottle()

# ----------------- Connessione PostgreSQL -----------------
PGHOST = os.getenv('PGHOST', 'localhost')
PGPORT = os.getenv('PGPORT', '5432')
PGDATABASE = os.getenv('PGDATABASE', 'bar_db')
PGUSER = os.getenv('PGUSER', 'bar_user')
PGPASSWORD = os.getenv('PGPASSWORD', 'bar_pwd')
DATABASE_URL = os.getenv('DATABASE_URL')  # opzionale: postgresql://user:pwd@host:port/db

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

# ----------------- Schema & dati demo -----------------
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS prodotti (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  prezzo_euro NUMERIC(10,2),
  attivo BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE IF NOT EXISTS posizioni (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS ordini (
  id SERIAL PRIMARY KEY,
  posizione_id INTEGER NOT NULL REFERENCES posizioni(id),
  stato TEXT NOT NULL DEFAULT 'NUOVO',
  creato_il TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  creato_da TEXT,
  totale_euro NUMERIC(10,2) DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ordine_righe (
  id SERIAL PRIMARY KEY,
  ordine_id INTEGER NOT NULL REFERENCES ordini(id) ON DELETE CASCADE,
  prodotto_id INTEGER NOT NULL REFERENCES prodotti(id),
  quantita INTEGER NOT NULL,
  nota TEXT,
  prezzo_euro_unit NUMERIC(10,2)
);
CREATE TABLE IF NOT EXISTS impostazioni (
  chiave TEXT PRIMARY KEY,
  valore TEXT
);
CREATE INDEX IF NOT EXISTS idx_ordini_stato_creato ON ordini (stato, creato_il);
"""

DEMO_DATA_SQL = [
    """
    INSERT INTO prodotti (nome, prezzo_euro, attivo)
    SELECT 'Caffè espresso', 1.00, TRUE
    WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Caffè espresso');
    """,
    """
    INSERT INTO prodotti (nome, prezzo_euro, attivo)
    SELECT 'Cappuccino', 1.50, TRUE
    WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Cappuccino');
    """,
    """
    INSERT INTO prodotti (nome, prezzo_euro, attivo)
    SELECT 'Brioche vuota', 1.20, TRUE
    WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Brioche vuota');
    """,
    """
    INSERT INTO prodotti (nome, prezzo_euro, attivo)
    SELECT 'Brioche crema', 1.30, TRUE
    WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Brioche crema');
    """,
    """
    INSERT INTO posizioni (nome) SELECT 'Sala Professori' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Sala Professori');
    """,
    """
    INSERT INTO posizioni (nome) SELECT 'Aula 1' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Aula 1');
    """,
    """
    INSERT INTO posizioni (nome) SELECT 'Aula 2' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Aula 2');
    """,
    """
    INSERT INTO posizioni (nome) SELECT 'Laboratorio 3' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Laboratorio 3');
    """,
    """
    INSERT INTO impostazioni (chiave, valore) VALUES ('BAR_APERTO', 'false')
    ON CONFLICT (chiave) DO NOTHING;
    """,
]

def init_db():
    con = get_conn()
    cur = con.cursor()
    try:
        # Esegui statements del DDL (multi)
        for stmt in SCHEMA_SQL.strip().split(";"):
            s = stmt.strip()
            if s:
                cur.execute(s + ";")
        # Dati demo
        for q in DEMO_DATA_SQL:
            cur.execute(q)
        con.commit()
    finally:
        cur.close()
        put_conn(con, commit=False)

# ----------------- Util -----------------

def bar_aperto():
    con = get_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("SELECT valore FROM impostazioni WHERE chiave='BAR_APERTO'")
        row = cur.fetchone()
        return row and row['valore'] == 'true'
    finally:
        cur.close()
        put_conn(con)

def set_bar(aperto: bool):
    con = get_conn()
    cur = con.cursor()
    try:
        cur.execute(
            """
            INSERT INTO impostazioni(chiave, valore)
            VALUES('BAR_APERTO', %s)
            ON CONFLICT(chiave) DO UPDATE SET valore=EXCLUDED.valore
            """,
            ("true" if aperto else "false",)
        )
        con.commit()
    finally:
        cur.close()
        put_conn(con, commit=False)

# ----------------- Template HTML (semplici) -----------------

TPL_BASE = """
<!doctype html>
<html lang=it>
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  % if refresh:
  <meta http-equiv=\"refresh\" content=\"{{refresh}}\">
  % end
  <title>{{title or 'Bar Scolastico'}}</title>
  <style>
    body{font-family: system-ui, sans-serif; background:#f8fafc; margin:0;}
    .wrap{max-width:720px;margin:0 auto;padding:16px;}
    .card{background:#fff;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:16px;margin:12px 0;}
    .btn{display:inline-block;background:#0ea5e9;color:#fff;border:none;border-radius:10px;padding:10px 14px;font-size:16px}
    .btn:disabled{background:#94a3b8}
    .btn2{background:#16a34a}
    .btn3{background:#f59e0b}
    .btn4{background:#3b82f6}
    .btn5{background:#64748b}
    label{display:block;margin:8px 0 4px;font-size:14px}
    select,input,textarea{width:100%;padding:10px;border:1px solid #cbd5e1;border-radius:10px;font-size:16px}
    .row{display:grid;grid-template-columns:1fr 90px 60px;gap:8px;align-items:end}
    .small{font-size:12px;color:#64748b}
    .title{font-weight:700;font-size:20px;margin:0 0 6px}
    .state{font-weight:700}
    ul{margin:8px 0 0 18px}
  </style>
</head>
<body>
  <div class=\"wrap\">
    {{!content}}
  </div>
</body>
</html>
"""

TPL_FORM = """
% rebase(TPL_BASE, title='Nuovo Ordine', refresh=None)
<div class=\"card\">
  <div class=\"title\">Bar scolastico</div>
  <div>Stato bar: <span class=\"state\">{{ 'APERTO' if aperto else 'CHIUSO' }}</span></div>
</div>

<div class=\"card\">
  <form method=\"post\" action=\"/ordina\">
    <label>Posizione attuale (aula)</label>
    <select name=\"posizione_id\" required>
      % for p in posizioni:
        <option value=\"{{p['id']}}\">{{p['nome']}}</option>
      % end
    </select>

    <label>Il tuo nome (docente)</label>
    <input name=\"creato_da\" placeholder=\"Es. Rossi\" required>

    <div id=\"righe\">
      % for i in range(1, iniziali+1):
      <div class=\"row\">
        <select name=\"prodotto_id_{{i}}\">
          % for pr in prodotti:
            <option value=\"{{pr['id']}}\">{{pr['nome']}}</option>
          % end
        </select>
        <input type=\"number\" name=\"quantita_{{i}}\" value=\"1\" min=\"1\">
        <input type=\"text\" name=\"nota_{{i}}\" placeholder=\"Nota\">
      </div>
      % end
    </div>

    <div class=\"small\">(Puoi aggiungere righe con il pulsante qui sotto)</div>
    <button type=\"button\" class=\"btn btn5\" onclick=\"addRow()\">+ Aggiungi prodotto</button>
    <br><br>
    <button class=\"btn btn2\" {{'disabled' if not aperto else ''}}>Invia ordine</button>
  </form>
</div>

<script>
  let idx = {{iniziali}};
  function addRow(){
    idx += 1;
    const r = document.createElement('div');
    r.className = 'row';
    r.innerHTML = `
      <select name=\"prodotto_id_${'{'}idx{'}'}\">
        ${'{'}[\
{% for pr in prodotti: %}
          \`<option value=\\\"{{pr['id']}}\\\">{{pr['nome']}}</option>\`,\
{% end %}
        ].join(''){'}'}
      </select>
      <input type=\"number\" name=\"quantita_${'{'}idx{'}'}\" value=\"1\" min=\"1\">
      <input type=\"text\" name=\"nota_${'{'}idx{'}'}\" placeholder=\"Nota\">
    `;
    document.getElementById('righe').appendChild(r);
  }
</script>
"""

TPL_DISPLAY = """
% rebase(TPL_BASE, title='Display Sala Bar', refresh=5)
<div class=\"card\">
  <div class=\"title\">Coda ordini</div>
  <div>Stato bar: <span class=\"state\" id=\"state\">{{ 'APERTO' if aperto else 'CHIUSO' }}</span></div>
  <form method=\"post\" action=\"/toggle\" style=\"margin-top:8px\">
    <button class=\"btn\">Aperto/Chiuso</button>
  </form>
</div>

% for o in ordini:
  <div class=\"card\">
    <div class=\"title\">#{{o['id']}} • {{o['posizione']}}</div>
    <div class=\"small\">Stato: {{o['stato']}} • {{o['creato_il']}}</div>
    <ul>
      % for r in o['righe']:
        <li>{{r['quantita']}}× {{r['prodotto']}}{{' – '+r['nota'] if r['nota'] else ''}}</li>
      % end
    </ul>
    <div style=\"margin-top:8px\">
      <form method=\"post\" action=\"/stato/{{o['id']}}/IN_PREPARAZIONE\" style=\"display:inline\"><button class=\"btn btn3\">Prepara</button></form>
      <form method=\"post\" action=\"/stato/{{o['id']}}/PRONTO\" style=\"display:inline\"><button class=\"btn btn2\">Pronto</button></form>
      <form method=\"post\" action=\"/stato/{{o['id']}}/CONSEGNATO\" style=\"display:inline\"><button class=\"btn btn4\">Consegnato</button></form>
      <form method=\"post\" action=\"/stato/{{o['id']}}/ANNULLATO\" style=\"display:inline\"><button class=\"btn btn5\">Annulla</button></form>
    </div>
  </div>
% end
"""

# ----------------- Rotte -----------------

@APP.get('/')
def form():
    con = get_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute('SELECT id, nome, prezzo_euro FROM prodotti WHERE attivo=true ORDER BY nome')
        prodotti = cur.fetchall()
        cur.execute('SELECT id, nome FROM posizioni ORDER BY nome')
        posizioni = cur.fetchall()
        return template(TPL_FORM, TPL_BASE=TPL_BASE, prodotti=prodotti, posizioni=posizioni, aperto=bar_aperto(), iniziali=2)
    finally:
        cur.close()
        put_conn(con)

@APP.post('/ordina')
def ordina():
    if not bar_aperto():
        return template(TPL_BASE, title='Bar chiuso', refresh=None, content='<div class="card"><b>Bar chiuso</b></div>')

    formd = request.forms
    posizione_id = int(formd.get('posizione_id'))
    creato_da = formd.get('creato_da') or ''

    # Estrai righe dinamiche
    righe = []
    for k in formd:
        if k.startswith('prodotto_id_'):
            idx = k.split('_')[-1]
            try:
                prod_id = int(formd.get(f'prodotto_id_{idx}'))
                q = int(formd.get(f'quantita_{idx}', '1'))
                nota = formd.get(f'nota_{idx}', '').strip() or None
            except (TypeError, ValueError):
                continue
            if q > 0:
                righe.append((prod_id, q, nota))

    if not righe:
        return template(TPL_BASE, title='Errore', refresh=None, content='<div class="card"><b>Nessun prodotto selezionato.</b></div>')

    con = get_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
    try:
        # Calcola totale
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
            cur.execute('SELECT prezzo_euro, nome FROM prodotti WHERE id=%s', (prod_id,))
            row = cur.fetchone()
            cur.execute('''
                INSERT INTO ordine_righe (ordine_id, prodotto_id, quantita, nota, prezzo_euro_unit)
                VALUES (%s,%s,%s,%s,%s)
            ''', (ordine_id, prod_id, q, nota, row['prezzo_euro']))

        con.commit()
    finally:
        cur.close()
        put_conn(con, commit=False)

    return redirect('/grazie')

@APP.get('/grazie')
def grazie():
    html = '<div class="card"><div class="title">Ordine inviato!</div><p>Grazie, la sala bar ha ricevuto la comanda.</p><a href="/" class="btn" style="margin-top:8px;display:inline-block">Nuovo ordine</a></div>'
    return template(TPL_BASE, title='Grazie', refresh=3, content=html)

@APP.get('/display')
@APP.get('/display/<stato>')
def display(stato=None):
    con = get_conn()
    cur = con.cursor(cursor_factory=RealDictCursor)
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
            righe = cur2.fetchall()
            cur2.close()
            result.append({
                'id': o['id'], 'stato': o['stato'], 'creato_il': o['creato_il'],
                'posizione': o['posizione'], 'righe': righe
            })
        return template(TPL_DISPLAY, TPL_BASE=TPL_BASE, ordini=result, aperto=bar_aperto())
    finally:
        cur.close()
        put_conn(con)

@APP.post('/stato/<oid:int>/<nuovo>')
def cambia_stato(oid, nuovo):
    con = get_conn()
    cur = con.cursor()
    try:
        cur.execute('UPDATE ordini SET stato=%s WHERE id=%s', (nuovo, oid))
        con.commit()
    finally:
        cur.close()
        put_conn(con, commit=False)
    return redirect('/display')

@APP.post('/toggle')
def toggle():
    nuovo = not bar_aperto()
    set_bar(nuovo)
    return redirect('/display')

@APP.get('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='./static')

if __name__ == '__main__':
    # In didattica: lascia attivo per creare tabelle e inserire dati demo
    init_db()
    print('Avvio su http://localhost:8080  (Display: /display)')
    run(APP, host='0.0.0.0', port=8080, reloader=True)
