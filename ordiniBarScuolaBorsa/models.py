from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import logging

db = SQLAlchemy()

# ===== MODELLO UTENTE (NUOVO) =====
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    nome = db.Column(db.String(100))
    cognome = db.Column(db.String(100))
    picture = db.Column(db.String(500))
    is_professor = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime)
    
    ordini = db.relationship('Ordine', back_populates='user', foreign_keys='Ordine.user_id')
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def get_price_type(self):
        """Ritorna il tipo di prezzo da usare"""
        return 'interni' if self.is_professor else 'pubblico'

# ===== MODELLI ESISTENTI =====
class Prodotto(db.Model):
    __tablename__ = 'prodotti'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    costo = db.Column(db.Numeric(10, 2))
    prezzo_euro = db.Column(db.Numeric(10, 2))
    margine = db.Column(db.Numeric(10, 2))
    prezzo_interni = db.Column(db.Numeric(10, 2))
    attivo = db.Column(db.Boolean, default=True, nullable=False)
    categoria = db.Column(db.String(100), nullable=True) 
    
    note_gruppi = db.relationship('NoteGruppo', back_populates='prodotto')
    
    def get_price(self, user=None):
        """Ritorna il prezzo corretto in base all'utente"""
        if user and user.is_professor:
            return float(self.prezzo_interni) if self.prezzo_interni else float(self.prezzo_euro)
        return float(self.prezzo_euro)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # NUOVO
    stato = db.Column(db.String, default='NUOVO', nullable=False)
    creato_il = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    creato_da = db.Column(db.String)
    totale_euro = db.Column(db.Numeric(10, 2), default=0)
    tipo_prezzo = db.Column(db.String(20), default='pubblico')  # NUOVO
    stato_pronto_da = db.Column(db.DateTime, nullable=True)  # Timestamp quando diventa PRONTO

    posizione = db.relationship('Posizione', back_populates='ordini')
    righe = db.relationship('OrdineRiga', back_populates='ordine', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='ordini', foreign_keys=[user_id])  # NUOVO

class OrdineRiga(db.Model):
    __tablename__ = 'ordine_righe'
    
    id = db.Column(db.Integer, primary_key=True)
    ordine_id = db.Column(db.Integer, db.ForeignKey('ordini.id'), nullable=False)
    prodotto_id = db.Column(db.Integer, db.ForeignKey('prodotti.id'), nullable=False)
    quantita = db.Column(db.Integer, nullable=False)
    prezzo_euro_unit = db.Column(db.Numeric(10, 2))

    ordine = db.relationship('Ordine', back_populates='righe')
    prodotto = db.relationship('Prodotto')
    note_righe = db.relationship('OrdineRigaNota', back_populates='riga', cascade="all, delete-orphan")

class OrdineRigaNota(db.Model):
    __tablename__ = 'ordine_righe_note'
    
    id = db.Column(db.Integer, primary_key=True)
    ordine_riga_id = db.Column(db.Integer, db.ForeignKey('ordine_righe.id'), nullable=False)
    nota_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    
    riga = db.relationship('OrdineRiga', back_populates='note_righe')

class Impostazione(db.Model):
    __tablename__ = 'impostazioni'
    
    chiave = db.Column(db.Text, primary_key=True)
    valore = db.Column(db.Text)

    def __repr__(self):
        return f"<Impostazione {self.chiave}>"

# ===== FUNZIONI DI UTILITÀ =====
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

def get_products(user=None):
    """
    Recupera i prodotti con i prezzi corretti in base all'utente
    COMPATIBILE con codice esistente (user è opzionale)
    """
    results = []

    query = db.session.query(
        Prodotto.id,
        Prodotto.nome.label('prodotto'),
        Prodotto.prezzo_euro,
        Prodotto.prezzo_interni,
        Prodotto.categoria,
        NoteGruppo.esclusivo,
        NoteGruppo.obbligatorio_default,
        Note.nome.label('nota')    
    ).join(NoteGruppo, Prodotto.id == NoteGruppo.id_prodotto, isouter=True) \
     .join(Note, NoteGruppo.id == Note.id_gruppo, isouter=True) \
     .filter(Prodotto.attivo == True).all()
    
    for item in query:
        # Determina quale prezzo mostrare
        if user and user.is_professor:
            prezzo_da_mostrare = item.prezzo_interni if item.prezzo_interni else item.prezzo_euro
        else:
            prezzo_da_mostrare = item.prezzo_euro
            
        results.append({
            'id': item.id,
            'prodotto': item.prodotto,
            'prezzo_euro': item.prezzo_euro,
            'prezzo_interni': item.prezzo_interni,
            'prezzo_mostrato': prezzo_da_mostrare,
            'categoria': item.categoria,
            'esclusivo': item.esclusivo,
            'obbligatorio_default': item.obbligatorio_default,
            'nota': item.nota
        })
    
    return results

def get_queue():
    """Recupera tutti gli ordini dalla coda con i loro dettagli"""
    try:
        ordini = db.session.query(Ordine).order_by(Ordine.creato_il.desc()).all()
        results = []

        for ordine in ordini:
            # Raggruppa tutte le righe (prodotti) per questo ordine
            righe = db.session.query(OrdineRiga).filter(OrdineRiga.ordine_id == ordine.id).all()
            items = []

            for riga in righe:
                prodotto = db.session.query(Prodotto).filter(Prodotto.id == riga.prodotto_id).first()
                note_query = db.session.query(Note).join(
                    OrdineRigaNota, Note.id == OrdineRigaNota.nota_id
                ).filter(OrdineRigaNota.ordine_riga_id == riga.id).all()

                # Se non ci sono note, mantieni almeno un elemento None per compatibilità
                if not note_query:
                    note_query = [None]

                for nota in note_query:
                    items.append({
                        'prodotto': prodotto.nome if prodotto else 'Prodotto sconosciuto',
                        'quantita': riga.quantita,
                        'nota': nota.nome if nota else None,
                        'prezzo_unit': float(riga.prezzo_euro_unit) if riga.prezzo_euro_unit else None
                    })

            # Informazioni utente
            user_info = ""
            if ordine.user:
                user_info = f"{ordine.user.nome} {ordine.user.cognome}"
                if ordine.user.is_professor:
                    user_info += " 👨‍🏫"

            results.append({
                'id': ordine.id,
                'items': items,
                'posizione': ordine.posizione.nome if ordine.posizione else 'N/A',
                'stato': ordine.stato,
                'totale_euro': float(ordine.totale_euro) if ordine.totale_euro else 0,
                'creato_il': ordine.creato_il.strftime('%d/%m/%Y %H:%M') if ordine.creato_il else '',
                'tipo_prezzo': ordine.tipo_prezzo if hasattr(ordine, 'tipo_prezzo') else 'pubblico',
                'utente': user_info or ordine.creato_da or 'Anonimo',
                'stato_pronto_da': ordine.stato_pronto_da.isoformat() if ordine.stato_pronto_da else None
            })

        return results

    except Exception as e:
        logging.error(f"Errore in get_queue: {str(e)}", exc_info=True)
        raise

def add_queue(posizione_id, righe, creato_da=None, totale_euro=None, stato='NUOVO', user=None):
    """
    Aggiunge un ordine alla coda
    COMPATIBILE con codice esistente + supporto autenticazione
    """
    try:
        # Determina il tipo di prezzo
        tipo_prezzo = 'interni' if (user and user.is_professor) else 'pubblico'
        
        # Se user è fornito e creato_da è None, usa i dati dell'utente
        if user and not creato_da:
            creato_da = f"{user.nome} {user.cognome}"
        
        new_order = Ordine(
            posizione_id=posizione_id, 
            stato=stato,
            user_id=user.id if user else None,
            creato_da=creato_da or 'system',
            tipo_prezzo=tipo_prezzo,
            totale_euro=totale_euro or 0
        )

        # Se righe è una lista, processala
        if isinstance(righe, list) and len(righe) > 0:
            for riga in righe:
                prodotto = db.session.query(Prodotto).filter(Prodotto.id == riga['prodotto_id']).first()
                if prodotto:
                    prezzo_unit = prodotto.get_price(user)
                    
                    ordine_riga = OrdineRiga(
                        prodotto_id=riga['prodotto_id'],
                        quantita=riga['quantita'],
                        prezzo_euro_unit=prezzo_unit
                    )
                    # Append to the parent collection so delete-orphan cascade
                    # does not treat the new row as an orphan before commit.
                    new_order.righe.append(ordine_riga)

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

# ===== FUNZIONI PER GESTIRE GLI UTENTI (NUOVO) =====
def get_or_create_user(google_id, email, nome, cognome, picture):
    """
    Trova un utente esistente o ne crea uno nuovo
    Determina automaticamente se è un professore dal dominio email
    """
    user = User.query.filter_by(google_id=google_id).first()
    
    if not user:
        # Verifica se l'email appartiene al dominio della scuola
        is_professor = email.endswith('@scuola-borsa.it')
        
        user = User(
            google_id=google_id,
            email=email,
            nome=nome,
            cognome=cognome,
            picture=picture,
            is_professor=is_professor
        )
        db.session.add(user)
        db.session.commit()
        logging.info(f"Nuovo utente creato: {email} (Professore: {is_professor})")
    else:
        # Aggiorna ultimo accesso
        user.last_login = db.func.now()
        db.session.commit()
    
    return user