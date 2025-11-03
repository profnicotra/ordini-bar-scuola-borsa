INSERT INTO prodotti (nome, prezzo_euro, attivo)
SELECT 'Caffè espresso', 1.00, TRUE
WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Caffè espresso');

INSERT INTO prodotti (nome, prezzo_euro, attivo)
SELECT 'Cappuccino', 1.50, TRUE
WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Cappuccino');

INSERT INTO prodotti (nome, prezzo_euro, attivo)
SELECT 'Brioche vuota', 1.20, TRUE
WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Brioche vuota');

INSERT INTO prodotti (nome, prezzo_euro, attivo)
SELECT 'Brioche crema', 1.30, TRUE
WHERE NOT EXISTS (SELECT 1 FROM prodotti WHERE nome='Brioche crema');

INSERT INTO posizioni (nome) SELECT 'Sala Professori' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Sala Professori');
INSERT INTO posizioni (nome) SELECT 'Aula 1' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Aula 1');
INSERT INTO posizioni (nome) SELECT 'Aula 2' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Aula 2');
INSERT INTO posizioni (nome) SELECT 'Laboratorio 3' WHERE NOT EXISTS (SELECT 1 FROM posizioni WHERE nome='Laboratorio 3');

INSERT INTO impostazioni (chiave, valore) VALUES ('BAR_APERTO', 'false')
ON CONFLICT (chiave) DO NOTHING;