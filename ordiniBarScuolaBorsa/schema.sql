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