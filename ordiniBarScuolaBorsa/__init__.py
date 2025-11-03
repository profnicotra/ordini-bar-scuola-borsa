from flask import Flask, render_template

from ordiniBarScuolaBorsa.models import db, Prodotto, Posizione, Ordine, OrdineRiga, Impostazione

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

import ordiniBarScuolaBorsa.index
import ordiniBarScuolaBorsa.menu
import ordiniBarScuolaBorsa.queue
import ordiniBarScuolaBorsa.orders
import ordiniBarScuolaBorsa.admin


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)