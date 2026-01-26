# Generatore Excel Codice Fiscale

Sistema automatico per generare file Excel 2016+ per il calcolo del Codice Fiscale.

## 📋 Funzionalità

- ✅ Generazione automatica file Excel 2016+
- ✅ Compatibile con Excel 2016, 2019, 365, LibreOffice Calc
- ✅ Due metodi di utilizzo: **CLI** e **Web Route**
- ✅ Include foglio con istruzioni e esempi
- ✅ Già compilato con 3 esempi

## 🚀 Come usare

### Metodo 1: CLI (Command Line)

**Generare l'Excel nel Download:**
```bash
python -m ordiniBarScuolaBorsa.cli_excel
```

**Specificare una cartella di destinazione:**
```bash
python -m ordiniBarScuolaBorsa.cli_excel -o "C:\Utenti\nomeutente\Desktop\MioFile.xlsx"
```

**Silenzioso (senza messaggi):**
```bash
python -m ordiniBarScuolaBorsa.cli_excel -q
```

### Metodo 2: Web Route

Se l'app Flask è in esecuzione, scarica l'Excel visitando:
```
http://localhost:5000/download-excel
```

### Metodo 3: Script Python diretto

```python
from ordiniBarScuolaBorsa.excel_generator import create_excel_cf_generator

# Genera nel Download
file_path = create_excel_cf_generator()
print(f"File creato: {file_path}")

# Oppure specifica il percorso
file_path = create_excel_cf_generator("/path/to/file.xlsx")
```

## 📦 Dipendenze

Assicurati di avere `openpyxl` installato:
```bash
pip install openpyxl
```

Se non è installato, il sistema proverà a installarlo automaticamente.

## 📊 Contenuto del file Excel

### Foglio 1: "Codice Fiscale"
| Colonna | Contenuto |
|---------|-----------|
| A | Cognome |
| B | Nome |
| C | CF Cognome (3 lettere) |
| D | CF Nome (3 lettere) |
| E | Data Nascita (GG/MM/YYYY) |
| F | Sesso (M/F) |

**Righe pre-compilate:** 3 esempi di utilizzo
**Righe vuote:** 16 righe disponibili per l'utente

### Foglio 2: "Istruzioni"
- Regole per estrarre il CF dal cognome
- Regole per estrarre il CF dal nome (con caso speciale 4+ consonanti)
- Esempi pratici

## 🔧 Dettagli Tecnici

### Excel 2016 vs Excel 365

**Excel 2016/2019:** Usa formule con `CONCATENA`, `IF`, `IFERROR`, `MATCH`
- ✅ Compatibile al 100%
- ❌ Formule più lunghe e complesse

**Excel 365:** Potrebbe usare `LET()`, `FILTER()`, `TESTO.DIVIDI()`
- ✅ Formule più compatte
- ❌ Non compatibile con versioni precedenti

Questo generatore produce file **compatibili con Excel 2016**, ma il file può essere aggiornato manualmente con le formule dinamiche per Excel 365 nel file HTML.

## 📝 Note

- Il file è salvato in formato `.xlsx` (OpenXML)
- I timestamp nel nome file evitano sovrascritture accidentali
- Le formule sono disabilitate di default per compatibilità
- Esegui `F9` in Excel per aggiornare tutte le formule

## 🐛 Troubleshooting

**Errore: "openpyxl not found"**
```bash
pip install openpyxl
```

**Il file non si scarica dalla web route**
- Assicurati che la route `/download-excel` sia registrata nel Blueprint
- Controlla che la app Flask sia avviata su `localhost:5000`

**Formule non funzionano in Excel 2016**
- Apri il file e premi `Ctrl+Shift+F9` per ricalcolare tutte le formule
- Verifica che il linguaggio di Excel sia impostato su Italiano (per `MAIUSC`, `CONCATENA`, ecc.)
