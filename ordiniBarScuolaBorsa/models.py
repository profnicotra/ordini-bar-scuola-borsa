from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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
    
def scriviOrdine():
    return NotImplementedError