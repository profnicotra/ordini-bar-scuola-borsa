CONFIGURAZIONE SERVER GRUPPO 2:
- Ambiente di sviluppo: VS Code con estensione "Live Server".
- Web Server locale: Apache (tramite XAMPP) per gestire script futuri.
- Database: MySQL per la persistenza dei dati delle note.
- Frontend: HTML5, CSS3, JavaScript ES6.
// Modello per gestire i gruppi di note
const modelloGruppi = ["Caffetteria", "Sezione Dolce", "Sezione Salato"];

// Modello per gestire le note all'interno dei gruppi
const modelloNote = [
    { id: 1, gruppo: "Caffetteria", prodotto: "Caffè Espresso", nota: "" },
    { id: 2, gruppo: "Dolce", prodotto: "Cornetto Crema", nota: "" },
    { id: 3, gruppo: "Salato", prodotto: "Focaccia Crudo", nota: "" }
];
<!-- Esempio di riga con input per la nota -->
<tr>
    <td><span class="nome-prod">Caffè Espresso</span></td>
    <td><input type="text" id="nota-1" class="input-note" placeholder="Aggiungi nota..."></td>
    <td><button onclick="salvaNota(1)">Salva</button></td>
</tr>
function caricaDatiReali() {
    // Questa funzione preleva i dati dal modello e li scrive nell'HTML
    console.log("Dati caricati sulla pagina HTML per il Gruppo 2");
    // Esempio: recupera una nota salvata
    document.getElementById('nota-1').value = localStorage.getItem('nota-1') || "";
}
window.onload = caricaDatiReali;
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
