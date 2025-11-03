from flask import Flask, render_template

from models import db, Prodotto, Posizione, Ordine, OrdineRiga, Impostazione

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)