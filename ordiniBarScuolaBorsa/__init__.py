from flask import Flask, render_template

from ordiniBarScuolaBorsa.models import db, Prodotto, Posizione, Ordine, OrdineRiga, Impostazione, is_bar_open, toggle_bar_open

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

import ordiniBarScuolaBorsa.index
import ordiniBarScuolaBorsa.menu
import ordiniBarScuolaBorsa.queue
import ordiniBarScuolaBorsa.orders
import ordiniBarScuolaBorsa.admin

with app.app_context():
    db.create_all()