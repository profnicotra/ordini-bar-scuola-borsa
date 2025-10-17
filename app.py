from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    prezzo_euro = db.Column(db.Numeric(10, 2))
    attivo = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Prodotto {self.nome}>"

class Posizione(db.Model):
    __tablename__ = 'posizioni'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"<Posizione {self.nome}>"

class Ordine(db.Model):
    __tablename__ = 'ordini'
    
    id = db.Column(db.Integer, primary_key=True)
    posizione_id = db.Column(db.Integer, db.ForeignKey('posizioni.id'), nullable=False)
    stato = db.Column(db.Text, nullable=False, default='NUOVO')
    creato_il = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    creato_da = db.Column(db.Text)
    totale_euro = db.Column(db.Numeric(10, 2), default=0)

    posizione = db.relationship('Posizione', backref='ordini')

    def __repr__(self):
        return f"<Ordine {self.id}>"

class OrdineRiga(db.Model):
    __tablename__ = 'ordine_righe'
    
    id = db.Column(db.Integer, primary_key=True)
    ordine_id = db.Column(db.Integer, db.ForeignKey('ordini.id', ondelete='CASCADE'), nullable=False)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)
    nota = db.Column(db.Text)
    prezzo_euro_unit = db.Column(db.Numeric(10, 2))

    ordine = db.relationship('Ordine', backref='righe')
    prodotto = db.relationship('Prodotto')

    def __repr__(self):
        return f"<OrdineRiga {self.id}>"

class Impostazione(db.Model):
    __tablename__ = 'impostazioni'
    
    chiave = db.Column(db.Text, primary_key=True)
    valore = db.Column(db.Text)

    def __repr__(self):
        return f"<Impostazione {self.chiave}>"
    
def insert_data():
    # Insert prodotti
    prodotti_data = [
        ('Caffè espresso', 1.00, True),
        ('Cappuccino', 1.50, True),
        ('Brioche vuota', 1.20, True),
        ('Brioche crema', 1.30, True)
    ]
    
    for nome, prezzo_euro, attivo in prodotti_data:
        if not Prodotto.query.filter_by(nome=nome).first():
            nuovo_prodotto = Prodotto(nome=nome, prezzo_euro=prezzo_euro, attivo=attivo)
            db.session.add(nuovo_prodotto)
    
    # Insert posizioni
    posizioni_data = ['Sala Professori', 'Aula 1', 'Aula 2', 'Laboratorio 3']
    
    for nome in posizioni_data:
        if not Posizione.query.filter_by(nome=nome).first():
            nuova_posizione = Posizione(nome=nome)
            db.session.add(nuova_posizione)
    
    # Insert impostazioni
    chiave, valore = 'BAR_APERTO', 'false'
    impostazione = Impostazione.query.get(chiave)
    if impostazione is None:
        impostazione = Impostazione(chiave=chiave, valore=valore)
        db.session.add(impostazione)
    
    # Commit the session
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        insert_data()
    app.run(debug=True)