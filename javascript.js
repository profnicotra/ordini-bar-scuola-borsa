// AGGIUNTA PER COLLEGAMENTO: Invia i dati alla memoria del browser
function sincronizzaDati() {
    let prodotti = [];
    document.querySelectorAll("tbody tr").forEach(row => {
        prodotti.push({
            nome: row.cells[0].innerText,
            prezzo: row.cells[2].innerText,
            attivo: row.cells[5].innerText,
            categoria: row.cells[6].innerText
        });
    });
    localStorage.setItem("datiBorsaBar", JSON.stringify(prodotti));
}

// Esegue la sincronizzazione ogni volta che scrivi o clicchi nella tabella
document.getElementById("table").addEventListener("input", sincronizzaDati);
document.getElementById("table").addEventListener("click", sincronizzaDati);
// Sincronizza anche all'avvio
window.addEventListener("load", sincronizzaDati);
