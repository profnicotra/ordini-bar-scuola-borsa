
from bottle import Bottle, static_file, TEMPLATE_PATH
import os

app = Bottle()

# Aggiunge la cartella 'views' al path dei template
VIEWS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'views'))
if VIEWS_DIR not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, VIEWS_DIR)

STATIC_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'static'))

@app.get('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root=STATIC_DIR)
