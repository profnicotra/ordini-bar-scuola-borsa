INSERT INTO prodotti (nome, ingredienti, costo, prezzo_vendita, prezzo_interno, categoria) VALUES
-- CAFFETTERIA
('Caffè Espresso', '7g Arabica miscela bar', 0.12, 1.20, 0.80, 'Caffè'),
('Cappuccino', 'Espresso + 120ml latte intero', 0.35, 1.50, 1.00, 'Caffè'),
('Spremuta Arancia', '3 Arance di Sicilia', 0.85, 4.00, 2.50, 'Fresh'),
('Spritz Aperol', 'Prosecco, Aperol, Soda', 1.20, 5.00, 3.50, 'Drink'),

-- DOLCE
('Cornetto Crema', 'Sfoglia burro artigianale', 0.60, 1.40, 1.00, 'Pastry'),
('Muffin Cioccolato', 'Con gocce di cioccolato fondente', 0.75, 2.50, 1.80, 'Pastry'),
('Fetta Crostata', 'Frolla e confettura di albicocca', 0.90, 3.00, 2.00, 'Dessert'),
('Cheesecake Bosco', 'Frolla e frutti rossi freschi', 1.30, 4.50, 3.00, 'Dessert');
INSERT INTO prodotti (nome, ingredienti, costo, prezzo_vendita, prezzo_interno, categoria) VALUES
-- CAFFETTERIA
('Caffè Espresso', '7g Arabica miscela bar', 0.12, 1.20, 0.80, 'Caffè'),
('Cappuccino', 'Espresso + 120ml latte intero', 0.35, 1.50, 1.00, 'Caffè'),
('Spremuta Arancia', '3 Arance di Sicilia', 0.85, 4.00, 2.50, 'Fresh'),
('Spritz Aperol', 'Prosecco, Aperol, Soda', 1.20, 5.00, 3.50, 'Drink'),

-- DOLCE
('Cornetto Crema', 'Sfoglia burro artigianale', 0.60, 1.40, 1.00, 'Pastry'),
('Muffin Cioccolato', 'Con gocce di cioccolato fondente', 0.75, 2.50, 1.80, 'Pastry'),
('Fetta Crostata', 'Frolla e confettura di albicocca', 0.90, 3.00, 2.00, 'Dessert'),
('Cheesecake Bosco', 'Frolla e frutti rossi freschi', 1.30, 4.50, 3.00, 'Dessert');
-- Esegui questa query per vedere l'analisi dei profitti aggiornata
SELECT 
    nome, 
    categoria, 
    (prezzo_vendita - costo) AS margine_profitto
FROM prodotti
ORDER BY margine_profitto DE;
