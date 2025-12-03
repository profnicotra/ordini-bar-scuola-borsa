from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    prezzo_euro = db.Column(db.Numeric(10, 2))
    margine = db.Column(db.Numeric(10, 2))
    prezzo_interni = db.Column(db.Numeric(10, 2))
    attivo = db.Column(db.Boolean, default=True, nullable=False)
    
    note_gruppi = db.relationship('NoteGruppo', back_populates='prodotto')

class Posizione(db.Model):
    __tablename__ = 'posizioni'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    ordini = db.relationship('Ordine', back_populates='posizione')

class NoteGruppo(db.Model):
    __tablename__ = 'note_gruppi'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    esclusivo = db.Column(db.Boolean, default=False, nullable=False)
    obbligatorio_default = db.Column(db.Boolean, default=False, nullable=False)
    id_prodotto = db.Column(db.Integer, db.ForeignKey('prodotti.id'), default=None)
    
    prodotto = db.relationship('Prodotto', back_populates='note_gruppi')
    note = db.relationship('Note', back_populates='gruppo')

class Note(db.Model):
    __tablename__ = 'note'
    
    id = db.Column(db.Integer, primary_key=True)
    id_gruppo = db.Column(db.Integer, db.ForeignKey('note_gruppi.id'), default=None)
    nome = db.Column(db.String, nullable=False)
    price_delta_euro = db.Column(db.Numeric(8, 2), default=0)
    
    gruppo = db.relationship('NoteGruppo', back_populates='note')

class Ordine(db.Model):
    __tablename__ = 'ordini'
    
    id = db.Column(db.Integer, primary_key=True)
    posizione_id = db.Column(db.Integer, db.ForeignKey('posizioni.id'), nullable=False)
    stato = db.Column(db.String, default='NUOVO', nullable=False)
    creato_il = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    creato_da = db.Column(db.String)
    totale_euro = db.Column(db.Numeric(10, 2), default=0)

    posizione = db.relationship('Posizione', back_populates='ordini')
    righe = db.relationship('OrdineRiga', back_populates='ordine')

class OrdineRiga(db.Model):
    __tablename__ = 'ordine_righe'
    
    id = db.Column(db.Integer, primary_key=True)
    ordine_id = db.Column(db.Integer, db.ForeignKey('ordini.id'), nullable=False)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)
    prezzo_euro_unit = db.Column(db.Numeric(10, 2))

    ordine = db.relationship('Ordine', back_populates='righe')
    prodotto = db.relationship('Prodotto')

class OrdineRigaNota(db.Model):
    __tablename__ = 'ordine_righe_note'
    
    id = db.Column(db.Integer, primary_key=True)
    ordine_riga_id = db.Column(db.Integer, db.ForeignKey('ordine_righe.id'), nullable=False)
    nota_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)

class Impostazione(db.Model):
    __tablename__ = 'impostazioni'
    
    chiave = db.Column(db.Text, primary_key=True)
    valore = db.Column(db.Text)

    def __repr__(self):
        return f"<Impostazione {self.chiave}>"