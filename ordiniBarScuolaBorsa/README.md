# Ordini Bar Scuola Borsa

Applicazione Flask con SQLite (predefinito) o database configurato tramite `DATABASE_URL`.

## Avvio

Dalla directory principale del repository:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r ordiniBarScuolaBorsa/requirements.txt
cp ordiniBarScuolaBorsa/.env.example ordiniBarScuolaBorsa/.env
python -m flask --app ordiniBarScuolaBorsa run --port 8080
```

Se `.env` esiste già, conservarlo e aggiungere soltanto le variabili mancanti.
Le variabili dell'ambiente hanno precedenza sul file `.env`.
Impostare una `SECRET_KEY` casuale e stabile, condivisa da tutti i processi dell'applicazione.

## Accesso Google e operatori

L'unico metodo di autenticazione è Google. Configurare `GOOGLE_CLIENT_ID` e
`GOOGLE_CLIENT_SECRET`, registrando il callback `/auth/callback` sull'origine del sito
(ad esempio `http://localhost:8080/auth/callback` in sviluppo).
Senza credenziali il sito resta consultabile e il login mostra un messaggio di indisponibilità.
Il callback accetta soltanto email verificate da Google.

`ADMIN_EMAILS` contiene gli indirizzi Google degli operatori, separati da virgole:

```dotenv
ADMIN_EMAILS=gestore@example.it,altro-gestore@example.it
```

Solo questi account possono aprire `/admin`, `/queue`, `/toggle` e usare le relative
operazioni. La lista vuota nega l'accesso a tutti. L'appartenenza al dominio dei
professori non assegna privilegi amministrativi. `DOMINIO_PROFESSORI` determina il
listino riservato.

Per attivare o disattivare la protezione dei pannelli usare nel `.env`:

```dotenv
REQUIRE_OPERATOR_LOGIN=true
```

`true` richiede login Google e presenza in `ADMIN_EMAILS`. `false` permette a
chiunque di accedere a `/admin`, `/queue`, `/toggle` e alle relative operazioni e
API, anche senza login. I token CSRF restano richiesti per le modifiche.
Se la variabile manca o ha un valore diverso da `false`, la protezione resta attiva.
Riavviare l'applicazione dopo modifiche alla configurazione.

Gli ospiti possono continuare a consultare e ordinare con nome e cognome.
Gli ordini richiedono token CSRF, ID dei prodotti e delle posizioni, quantità intere
tra 1 e 10, e varianti valide. Prezzi, supplementi e totale vengono calcolati sul
server. Un carrello non valido viene rifiutato interamente; a bar chiuso gli ordini
sono rifiutati con HTTP 409. Il vecchio carrello basato sui nomi va ricreato dal menù.

## Verifiche

```sh
python -m unittest discover -s tests -v
```

I test usano SQLite in memoria e non modificano `instance/data.db`.
Node.js è richiesto per i test JavaScript dell'admin. Le verifiche OAuth simulano
le risposte Google; il login reale richiede credenziali valide e callback configurato.

Questa correzione non introduce migrazioni del database. La persistenza delle
note generali libere e il layout mobile dell'admin restano interventi separati.
