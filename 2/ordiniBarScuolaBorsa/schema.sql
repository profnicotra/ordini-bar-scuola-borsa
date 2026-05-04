CREATE TABLE IF NOT EXISTS prodotti (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL,
  prezzo_euro NUMERIC (10,2),
  margine NUMERIC(10,2),
  prezzo_interni NUMERIC(10,2)
  attivo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS posizioni (
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS  note_gruppi(
  id SERIAL PRIMARY KEY,
  nome TEXT NOT NULL UNIQUE,
  esclusivo BOOLEAN NOT NULL DEFAULT FALSE,
  obbligatorio_default BOOLEAN NOT NULL DEFAULT FALSE,
  id_prodotto INTEGER REFERENCES prodotti (id) ON DELETE CASCADE DEFAULT NULL
);

  
CREATE TABLE IF NOT EXISTS  note (
  id SERIAL PRIMARY KEY,
  id_gruppo INTEGER REFERENCES note_gruppi  (id) ON DELETE CASCADE DEFAULT NULL,
  nome TEXT NOT NULL,
  price_delta_euro NUMERIC(8,2) DEFAULT 0,
  UNIQUE (id_gruppo, name),
);

CREATE TABLE IF NOT EXISTS stati (
  id SERIAL PRIMARY KEY,
  
)

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
  prezzo_euro_unit NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS ordine_righe_note (
  id SERIAL PRIMARY KEY,
  ordine_riga_id INTEGER NOT NULL REFERENCES ordini_riga(id) ON DELETE CASCADE,
  nota_id  INTEGER NOT NULL REFERENCES nota(id) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS impostazioni (
  chiave TEXT PRIMARY KEY,
  valore TEXT
);
CREATE INDEX IF NOT EXISTS idx_ordini_stato_creato ON ordini (stato, creato_il);

--Query per verificare se bar è aperto
SELECT valore from impostazioni where chiave = 'bar_aperto';

--Query per aprire bar
UPDATE impostazioni SET valore = 'true' where chiave = 'bar_aperto';

--Query per chiudere bar
UPDATE impostazioni SET valore = 'false' where chiave = 'bar_aperto';

--Query per chiudere bar
UPDATE impostazioni SET valore = 'false' where chiave = 'bar_aperto';

--Query estrazione note generali
SELECT n.nome nota
FROM note n 
WHERE id_gruèèp IS NULL;

--Query estrazione prodotti
SELECT p.nome prodotto, p.prezzo_euro, p.prezzo_interni, ng.esclusivo, ng.obbligatorio_default, n.nome nota,
FROM prodotti p
JOIN note_gruppi ng ON p.id = ng.id_prodotto
JOIN note n ON p.id = ng.id_prodotto
WHERE p.attivo = 1;
  
--query estrazione coda
SELECT o.id, pr.nome prodotto, ori.quantita, n.nota nota, pos.nome posizione, o.stato, o.totale_euro
FROM ordini o
JOIN ordine_righe ori ON o.id = ori.ordine_id
JOIN ordine_righe_note orn ON ori.id = orn.ordine_riga_id
JOIN note n ON orn.nota_id = n.id
JOIN posizioni pos ON pos.id = o.posizione_id
JOIN prodotti pr ON pr.id = ori.prodotto_id;
