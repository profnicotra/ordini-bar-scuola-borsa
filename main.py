
from bottle import run
from app import app
from app.init_db import init_db

# registra le rotte importando i moduli
import app.routes_order  # noqa: F401
import app.routes_display  # noqa: F401
import app.routes_bar  # noqa: F401

if __name__ == '__main__':
    init_db()
    print('Avvio su http://localhost:8080  (Display: /display)')
    run(app, host='0.0.0.0', port=8080, reloader=True)
