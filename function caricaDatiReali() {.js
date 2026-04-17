function caricaDatiReali() {
    // Questa funzione preleva i dati dal modello e li scrive nell'HTML
    console.log("Dati caricati sulla pagina HTML per il Gruppo 2");
    // Esempio: recupera una nota salvata
    document.getElementById('nota-1').value = localStorage.getItem('nota-1') || "";
}
window.onload = caricaDatiReali;
