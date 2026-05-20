from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import logging

db = SQLAlchemy()

# ==============================================================================
# 1. MODELLO UTENTE (Gestione Accessi e Ruoli)
# ==============================================================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))      # Mantenuto 'nome' nel DB
    nome = name # Alias per compatibilità con il resto del codice
    cognome = db.Column(db.String(100))
    picture = db.Column(db.String(500))
    is_professor = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_login = db.Column(db.DateTime)
    
    ordini = db.relationship('Ordine', back_populates='user', foreign_keys='Ordine.user_id')
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def get_price_type(self):
        """Ritorna il tipo di prezzo da usare in base al ruolo"""
        return 'interni' if self.is_professor else 'pubblico'


# ==============================================================================
# 2. MODELLI MENU (Prodotti, Categorie e Varianti)
# ==============================================================================
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
    
    note_gruppi = db.relationship('NoteGruppo', back_populates='prodotto', cascade="all, delete-orphan")
    
    def get_price(self, user=None):
        """Ritorna il prezzo corretto in base all'utente"""
        if user and user.is_professor:
            return float(self.prezzo_interni) if self.prezzo_interni else float(self.prezzo_euro)
        return float(self.prezzo_euro)


class NoteGruppo(db.Model):
    __tablename__ = 'note_gruppi'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)
    esclusivo = db.Column(db.Boolean, default=False, nullable=False)
    obbligatorio_default = db.Column(db.Boolean, default=False, nullable=False)
    id_prodotto = db.Column(db.Integer, db.ForeignKey('prodotti.id'), default=None)
    
    prodotto = db.relationship('Prodotto', back_populates='note_gruppi')
    # AGGIUNTO CASCADE: se elimini il gruppo, cancella automaticamente le sue note dal DB
    note = db.relationship('Note', back_populates='gruppo', cascade="all, delete-orphan")


class Note(db.Model):
    __tablename__ = 'note'
    
    id = db.Column(db.Integer, primary_key=True)
    id_gruppo = db.Column(db.Integer, db.ForeignKey('note_gruppi.id'), default=None)
    nome = db.Column(db.String, nullable=False)
    price_delta_euro = db.Column(db.Numeric(8, 2), default=0)
    
    gruppo = db.relationship('NoteGruppo', back_populates='note')


class Posizione(db.Model):
    __tablename__ = 'posizioni'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    
    ordini = db.relationship('Ordine', back_populates='posizione')


# ==============================================================================
# 3. MODELLI ORDINI (Coda e Carrello)
# ==============================================================================
class Ordine(db.Model):
    __tablename__ = 'ordini'
    
    id = db.Column(db.Integer, primary_key=True)
    posizione_id = db.Column(db.Integer, db.ForeignKey('posizioni.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    stato = db.Column(db.String, default='NUOVO', nullable=False)
    creato_il = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    creato_da = db.Column(db.String)
    totale_euro = db.Column(db.Numeric(10, 2), default=0)
    tipo_prezzo = db.Column(db.String(20), default='pubblico')
    stato_pronto_da = db.Column(db.DateTime, nullable=True) 

    posizione = db.relationship('Posizione', back_populates='ordini')
    righe = db.relationship('OrdineRiga', back_populates='ordine', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='ordini', foreign_keys=[user_id]) 


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


# ==============================================================================
# 4. MODELLO IMPOSTAZIONI DI SISTEMA (Stato del Bar)
# ==============================================================================
class Impostazione(db.Model):
    __tablename__ = 'impostazioni'
    
    chiave = db.Column(db.Text, primary_key=True)
    valore = db.Column(db.Text)

    def __repr__(self):
        return f"<Impostazione {self.chiave}>"


# ==============================================================================
# 5. FUNZIONI DI UTILITÀ (Query di Sistema)
# ==============================================================================
def is_bar_open():
    """Verifica se il bar è aperto leggendo le impostazioni"""
    bar_aperto = Impostazione.query.filter_by(chiave="bar_aperto").first()
    if bar_aperto:
        return bar_aperto.valore
    return None

def toggle_bar_open():
    """Inverte lo stato di apertura del bar"""
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

def get_products(user=None, for_admin=False):
    """
    Recupera i prodotti con i prezzi corretti in base all'utente.
    Se for_admin=True, restituisce TUTTI i prodotti e anche costo/disponibilità.
    """
    results = []

    q = db.session.query(
        Prodotto.id,
        Prodotto.nome.label('prodotto'),
        Prodotto.costo,
        Prodotto.prezzo_euro,
        Prodotto.prezzo_interni,
        Prodotto.categoria,
        Prodotto.attivo,
        NoteGruppo.esclusivo,
        NoteGruppo.obbligatorio_default,
        Note.nome.label('nota')    
    ).join(NoteGruppo, Prodotto.id == NoteGruppo.id_prodotto, isouter=True) \
     .join(Note, NoteGruppo.id == Note.id_gruppo, isouter=True)
    
    if not for_admin:
        q = q.filter(Prodotto.attivo == True)
        
    query = q.all()
    
    for item in query:
        if user and user.is_professor:
            prezzo_da_mostrare = item.prezzo_interni if item.prezzo_interni else item.prezzo_euro
        else:
            prezzo_da_mostrare = item.prezzo_euro
            
        results.append({
            'id': item.id,
            'prodotto': item.prodotto,
            'costo': float(item.costo) if item.costo else 0,
            'prezzo_euro': float(item.prezzo_euro) if item.prezzo_euro else 0,
            'prezzo_interni': float(item.prezzo_interni) if item.prezzo_interni else 0,
            'prezzo_mostrato': float(prezzo_da_mostrare) if prezzo_da_mostrare else 0,
            'categoria': item.categoria,
            'attivo': item.attivo, 
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
            righe = db.session.query(OrdineRiga).filter(OrdineRiga.ordine_id == ordine.id).all()
            items = []

            for riga in righe:
                prodotto = db.session.query(Prodotto).filter(Prodotto.id == riga.prodotto_id).first()
                note_query = db.session.query(Note).join(
                    OrdineRigaNota, Note.id == OrdineRigaNota.nota_id
                ).filter(OrdineRigaNota.ordine_riga_id == riga.id).all()

                if not note_query:
                    note_query = [None]

                for nota in note_query:
                    items.append({
                        'prodotto': prodotto.nome if prodotto else 'Prodotto sconosciuto',
                        'quantita': riga.quantita,
                        'nota': nota.nome if nota else None,
                        'prezzo_unit': float(riga.prezzo_euro_unit) if riga.prezzo_euro_unit else None
                    })

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
    """Aggiunge un ordine alla coda calcolando il listino corretto"""
    try:
        tipo_prezzo = 'interni' if (user and user.is_professor) else 'pubblico'
        
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
                    new_order.righe.append(ordine_riga)

        db.session.add(new_order)
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Errore in add_queue: {str(e)}", exc_info=True)
        db.session.rollback()
        return False

def get_all_positions():
    """Recupera l'elenco delle posizioni/tavoli disponibili"""
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
    """Recupera le varianti globali slegate da uno specifico prodotto"""
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


# ==============================================================================
# 6. GESTIONE UTENTI (Riconoscimento automatico Professore)
# ==============================================================================
def get_or_create_user(google_id, email, nome, cognome, picture):
    """Trova un utente esistente o ne crea uno nuovo controllando il dominio della scuola"""
    user = User.query.filter_by(google_id=google_id).first()
    
    if not user:
        # Verifica se l'email appartiene ai professori
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
        user.last_login = db.func.now()
        db.session.commit()
    
    return user