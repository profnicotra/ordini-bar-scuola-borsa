CREATE DATABASE scuola_bar;
USE scuola_bar;

CREATE TABLE note_prodotti (
    id INT PRIMARY KEY,
    prodotto VARCHAR(255),
    gruppo VARCHAR(100),
    testo_nota TEXT
);

-- Esempio inserimento dati
INSERT INTO note_prodotti (id, prodotto, gruppo, testo_nota) 
VALUES (1, 'Caffè Espresso', 'Caffetteria', 'Servire caldo');
