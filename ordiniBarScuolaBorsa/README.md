
# Bar App – Bottle + PostgreSQL (didattico)

Due varianti:
- **single-file/**: tutto in un file (`app_pg.py`).
- **split-version/**: struttura a più file con template e SQL separati.

## Requisiti
```
pip install -r requirements.txt
```

## Variabili ambiente (oppure usa .env)
```
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=bar_db
export PGUSER=bar_user
export PGPASSWORD=bar_pwd
```

## Avvio (single-file)
```
cd single-file
python app_pg.py
```
- Ordine: http://localhost:8080/
- Display: http://localhost:8080/display

## Avvio (split-version)
```
cd split-version
python main.py
```
