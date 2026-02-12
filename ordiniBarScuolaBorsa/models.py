from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    costo = db.Column(db.Numeric(10, 2))
    prezzo_euro = db.Column(db.Numeric(10, 2))
    margine = db.Column(db.Numeric(10, 2))
    prezzo_interni = db.Column(db.Numeric(10, 2))
    attivo = db.Column(db.Boolean, default=True, nullable=False)
    
    # Nuova colonna aggiunta
    categoria = db.Column(db.String(100), nullable=True) 
    
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
    
def is_bar_open():
    bar_aperto = Impostazione.query.filter_by(chiave="bar_aperto").first()
    if bar_aperto:
        return bar_aperto.valore
    return None

def toggle_bar_open():
    setting = Impostazione.query.filter_by(chiave="bar_aperto").first()
    if setting:
        new_value = 'false' if setting.valore.lower() == 'true' else 'true'
        setting.valore = new_value
        db.session.commit()
        return new_value
    else:
        new_setting = Impostazione(chiave='bar_aperto', valore='true')
        db.session.add(new_setting)
        db.session.commit()
        return 'true'
    
def get_products():
    results = []

    query = db.session.query(
        Prodotto.nome.label('prodotto'),
        Prodotto.prezzo_euro,
        Prodotto.prezzo_interni,
        Prodotto.categoria,  # <-- 1. Aggiunto alla query
        NoteGruppo.esclusivo,
        NoteGruppo.obbligatorio_default,
        Note.nome.label('nota')    
    ).join(NoteGruppo, Prodotto.id == NoteGruppo.id_prodotto, isouter=True) \
     .join(Note, NoteGruppo.id == Note.id_gruppo, isouter=True) \
     .filter(Prodotto.attivo == True).all()
    
    for item in query:
        results.append({
            'prodotto': item.prodotto,
            'prezzo_euro': item.prezzo_euro,
            'prezzo_interni': item.prezzo_interni,
            'categoria': item.categoria, # <-- 2. Aggiunto al dizionario
            'esclusivo': item.esclusivo,
            'obbligatorio_default': item.obbligatorio_default,
            'nota': item.nota
        })
    
    return results

def get_queue():
    """Recupera tutti gli ordini dalla coda con i loro dettagli"""
    try:
        # Primo: prendi tutti gli ordini
        ordini = db.session.query(Ordine).order_by(Ordine.creato_il.desc()).all()
        
        results = []
        
        for ordine in ordini:
            # Per ogni ordine, prendi le righe
            righe = db.session.query(OrdineRiga).filter(OrdineRiga.ordine_id == ordine.id).all()
            
            for riga in righe:
                # Per ogni riga, prendi il prodotto
                prodotto = db.session.query(Prodotto).filter(Prodotto.id == riga.prodotto_id).first()
                
                # Per ogni riga, prendi le note
                note_query = db.session.query(Note).join(
                    OrdineRigaNota, Note.id == OrdineRigaNota.nota_id
                ).filter(OrdineRigaNota.ordine_riga_id == riga.id).all()
                
                # Se non ci sono note, crea un record comunque
                if not note_query:
                    note_query = [None]
                
                for nota in note_query:
                    results.append({
                        'id': ordine.id,
                        'prodotto': prodotto.nome if prodotto else 'Prodotto sconosciuto',
                        'quantita': riga.quantita,
                        'nota': nota.nome if nota else None,
                        'posizione': ordine.posizione.nome if ordine.posizione else 'N/A',
                        'stato': ordine.stato,
                        'totale_euro': float(ordine.totale_euro) if ordine.totale_euro else 0,
                        'creato_il': ordine.creato_il.strftime('%d/%m/%Y %H:%M') if ordine.creato_il else ''
                    })
        
        return results

    except Exception as e:
        logging.error(f"Errore in get_queue: {str(e)}", exc_info=True)
        raise

def add_queue(posizione_id, righe, creato_da, totale_euro, stato='NUOVO'  ):
    try:
        new_order = Ordine(
            posizione_id=posizione_id, 
            stato=stato, 
            creato_da=creato_da,
            totale_euro=totale_euro
        )

        for riga in righe:
            ordine_riga = OrdineRiga(
                prodotto_id=riga['prodotto_id'], 
                quantita=riga['quantita'], 
                ordine=new_order,
                prezzo_euro_unit=0
            )
            db.session.add(ordine_riga)

        db.session.add(new_order)
        db.session.commit()
        
        return True
    except Exception as e:
        logging.error(f"Errore in add_queue: {str(e)}", exc_info=True)
        db.session.rollback()
        return False
    
def get_all_positions():
    try:
        positions = db.session.query(Posizione).all()
        
        results = []
        for position in positions:
            results.append({
                'id': position.id,
                'nome': position.nome
            })
        
        return results
    except Exception as e:
        logging.error(f"Errore in get_all_positions: {str(e)}", exc_info=True)
        return []

def get_general_notes():
    try:
        note_gruppi = db.session.query(NoteGruppo).filter(
            NoteGruppo.id_prodotto == None
        ).all()
        
        results = []
        
        for gruppo in note_gruppi:
            note = db.session.query(Note).filter(
                Note.id_gruppo == gruppo.id
            ).all()
            
            results.append({
                'id_gruppo': gruppo.id,
                'nome_gruppo': gruppo.nome,
                'esclusivo': gruppo.esclusivo,
                'obbligatorio_default': gruppo.obbligatorio_default,
                'note': [
                    {
                        'id': n.id,
                        'nome': n.nome,
                        'price_delta_euro': float(n.price_delta_euro) if n.price_delta_euro else 0
                    }
                    for n in note
                ]
            })
        
        return results
    
    except Exception as e:
        logging.error(f"Errore in get_general_notes: {str(e)}", exc_info=True)
        return []