CREATE TABLE IF NOT EXISTS prodotti
(
id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, costo REAL, prezzo_euro REAL, margine REAL, prezzo_interni REAL, attivo INTEGER NOT NULL DEFAULT 1 );

DELETE FROM PRODOTTI;
INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo,  prezzo_euro, margine, prezzo_interni) VALUES ('espresso macchiato',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso macchiato soia',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso macchiato soia',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso macchiato',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso decaffeinato',0, 1.10, 1.10, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso doppio',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('espresso corretto',0, 1.50, 1.50, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino soia',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino no lattosio',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino decaffeinato',0, 1.60, 1.60, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino decaffeinato soia',0, 1.60, 1.60, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino decaffeinato no lattosio',0, 1.60, 1.60, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino orzo',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino ginseng',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino aromatizzato',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino decaffeinato',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cappuccino freddo',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('marocchino',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('marocchino soia',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('marocchino no lattosio',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('nutellino',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte bianco',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte bianco soia',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte bianco no lattosio',0, 1, 1, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte macchiato',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte macchiato soia',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte macchiato no lattosio',0, 1.80, 1.80, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('latte macchiato aromatizzato',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('caffelatte',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('caffelatte soia',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('caffelatte no lattosio',0, 1.50, 1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cioccolata calda',0, 2.50, 2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('cioccolata calda + panna',0, 3, 3, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('ciccolata calda aromatizzata',0, 3, 3, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('the caldo',0, 1.50, 1.50, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('camomilla',0, 1.50, 1.50, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('crema caffè',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('acqua bicc naturale',0, 0.20, 0.20, 0.00);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('acqua bicc frizz',0, 0.20, 0.20, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('succo arancia',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('succo pera',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('succo ananas',0, 2, 2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('spremuta arancia',0, 3, 3, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('caffè shakerato',0, 3, 3, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('caffè shakerato aromatizzato',0, 3, 3, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('orzo piccolo',0, 1.10, 1.10, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('orzo grande',0, 1.30, 1.30, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('ginseng piccolo',0, 1.10, 1.10, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('ginseng grande',0, 1.30, 1.30, 0.5);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('piccolino nutella',0, 2.50, 2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('piccolino pistacchio',0, 2.50, 2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('piccolino cioccolato',0, 2.50, 2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('piccolino caramello',0, 2.50,  2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('piccolino nocciola',0, 2.50,  2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche vuota', 0.50,  1.20,  0.70, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche nutella', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche albicocca', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche frutti di bosco', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche crema', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche integrale vuota', 0.50,  1.20, 0.70, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche integrale nutella', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche integrale albicocca', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche integrale frutti di bosco', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche integrale crema', 0.50,  1.50,  1, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche premium',0, 2,  2, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('muffin',0, 1.50,  1.50, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('fetta di torta', 0, 2,  2, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('frollino',0,  0.50,  0.50, 0.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('toast',0, 2.50, 2.50, 1.50);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('pizza',0, 2,  2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('focaccia',0, 2,  2, 1);

INSERT INTO prodotti (nome, costo, prezzo_euro, margine, prezzo_interni) VALUES ('brioche salata',0, 3,  3, 1.50);
DELETE FROM  Posizioni;
INSERT INTO posizioni (nome) VALUES ('banco bar');

INSERT INTO posizioni (nome) VALUES ('tavolo 1');

INSERT INTO posizioni (nome) VALUES ('tavolo 2');

INSERT INTO posizioni (nome) VALUES ('tavolo 3');

INSERT INTO posizioni (nome) VALUES ('tavolo 4');

INSERT INTO posizioni (nome) VALUES ('tavolo 5');

INSERT INTO posizioni (nome) VALUES ('tavolo 6');

INSERT INTO posizioni (nome) VALUES ('tavola 7');

INSERT INTO posizioni (nome) VALUES ('tavolo 8');

INSERT INTO posizioni (nome) VALUES ('tavolo 9');

INSERT INTO posizioni (nome) VALUES ('tavolo 10');

INSERT INTO posizioni (nome) VALUES ('tavolo 11');

INSERT INTO posizioni (nome) VALUES ('tavolo 12');

INSERT INTO posizioni (nome) VALUES ('tavolo 13');

INSERT INTO posizioni (nome) VALUES ('tavolo 14');

INSERT INTO posizioni (nome) VALUES ('tavolo 15');

INSERT INTO posizioni (nome) VALUES ('segreteria');

INSERT INTO posizioni (nome) VALUES ('segreteria ente');

INSERT INTO posizioni (nome) VALUES ('ufficio personale');

INSERT INTO posizioni (nome) VALUES ('uff. tutor P.T.');

INSERT INTO posizioni (nome) VALUES ('segreteria didattica');

INSERT INTO posizioni (nome) VALUES ('uff. coordinamento');

INSERT INTO posizioni (nome) VALUES ('uff. amministrazione');

INSERT INTO posizioni (nome) VALUES ('uff. tutor 1P .');

INSERT INTO posizioni (nome) VALUES ('direzione');

INSERT INTO posizioni (nome) VALUES ('sala professori 2p .');

INSERT INTO posizioni (nome) VALUES ('1BC');

INSERT INTO posizioni (nome) VALUES ('2BC');

INSERT INTO posizioni (nome) VALUES ('3BC');

INSERT INTO posizioni (nome) VALUES ('4BC');

INSERT INTO posizioni (nome) VALUES ('1A');

INSERT INTO posizioni (nome) VALUES ('2A');

INSERT INTO posizioni (nome) VALUES ('3A');

INSERT INTO posizioni (nome) VALUES ('4A');

INSERT INTO posizioni (nome) VALUES ('1D');

INSERT INTO posizioni (nome) VALUES ('2D');

INSERT INTO posizioni (nome) VALUES ('3D');

INSERT INTO posizioni (nome) VALUES ('4D');

INSERT INTO posizioni (nome) VALUES ('1PPD');

INSERT INTO posizioni (nome) VALUES ('2PPD');

INSERT INTO posizioni (nome) VALUES ('3PPD');

DELETE FROM note;

INSERT INTO note (nome) VALUES ('subito!');

INSERT INTO note (nome) VALUES ('offerto');

INSERT INTO note (nome) VALUES ('senza glutine');

INSERT INTO note (nome) VALUES ('senza lattosio');

INSERT INTO note (nome) VALUES ('vegano');

INSERT INTO note (nome) VALUES ('vegetariano');
