"""
auth.py - Blueprint per autenticazione Google OAuth
Bar Scuola Borsa - Gestione login/logout professori e studenti
"""

from flask import Blueprint, redirect, url_for, session, flash, request
from flask_login import login_user, logout_user, current_user
from authlib.integrations.flask_client import OAuth
from werkzeug.security import gen_salt
import os
from .models import db, User

# Crea Blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Inizializza OAuth (verrà configurato in __init__.py)
oauth = OAuth()

def init_oauth(app):
    """
    Inizializza OAuth con le credenziali Google
    Chiamata da __init__.py quando l'app viene creata
    """
    oauth.init_app(app)
    
    # Configura Google OAuth
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


@bp.route('/login')
def login():
    """
    Inizia il flusso OAuth con Google
    Reindirizza l'utente alla pagina di login Google
    """
    # Controlla se l'utente è già loggato
    if current_user.is_authenticated:
        flash('Sei già autenticato!', 'info')
        return redirect(url_for('menu.menu'))
    
    # Genera nonce per sicurezza
    nonce = gen_salt(16)
    session['nonce'] = nonce
    
    # URL di callback dopo il login Google
    redirect_uri = url_for('auth.callback', _external=True)
    
    # Reindirizza a Google per autenticazione
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)


@bp.route('/callback')
def callback():
    """
    Callback dopo l'autenticazione Google
    Riceve i dati dell'utente e crea/aggiorna l'account
    """
    try:
        # Ottieni token da Google
        token = oauth.google.authorize_access_token()
        
        # Verifica nonce per sicurezza
        nonce = session.pop('nonce', None)
        if not nonce:
            flash('Errore di autenticazione: sessione non valida', 'danger')
            return redirect(url_for('index.index'))
        
        # Ottieni informazioni utente
        user_info = oauth.google.parse_id_token(token, nonce=nonce)
        
        # Estrai dati
        email = user_info.get('email')
        nome = user_info.get('name', '')
        google_id = user_info.get('sub')  # Google User ID
        
        if not email or not google_id:
            flash('Impossibile ottenere informazioni dall\'account Google', 'danger')
            return redirect(url_for('index.index'))
        
        # Determina se è un professore (dominio @scuola-borsa.it)
        dominio_professori = os.getenv('DOMINIO_PROFESSORI', 'scuola-borsa.it')
        is_professore = email.endswith(f'@{dominio_professori}')
        
        # Cerca utente esistente
        user = User.query.filter_by(google_id=google_id).first()
        
        if user:
            # Aggiorna informazioni se cambiate
            user.email = email
            user.nome = nome
            user.is_professore = is_professore
        else:
            # Crea nuovo utente
            user = User(
                google_id=google_id,
                email=email,
                nome=nome,
                is_professore=is_professore
            )
            db.session.add(user)
        
        # Salva modifiche
        db.session.commit()
        
        # Login utente con Flask-Login
        login_user(user, remember=True)
        
        # Messaggio di benvenuto
        tipo = "professore" if is_professore else "studente"
        flash(f'Benvenuto {nome}! Accesso effettuato come {tipo}.', 'success')
        
        # Reindirizza al menu
        return redirect(url_for('menu.menu'))
        
    except Exception as e:
        # Log errore (in produzione usa logging appropriato)
        print(f"Errore durante autenticazione: {str(e)}")
        flash('Errore durante l\'autenticazione. Riprova.', 'danger')
        return redirect(url_for('index.index'))


@bp.route('/logout')
def logout():
    """
    Logout utente
    Cancella sessione Flask-Login
    """
    if current_user.is_authenticated:
        nome = current_user.nome
        logout_user()
        flash(f'Arrivederci {nome}! Disconnessione effettuata.', 'info')
    else:
        flash('Non eri autenticato.', 'warning')
    
    return redirect(url_for('index.index'))


@bp.route('/profile')
def profile():
    """
    Mostra profilo utente (opzionale)
    Puoi usarlo per debug o per una pagina profilo
    """
    if not current_user.is_authenticated:
        flash('Devi effettuare il login per vedere il profilo', 'warning')
        return redirect(url_for('auth.login'))
    
    # Informazioni utente
    info = {
        'Nome': current_user.nome,
        'Email': current_user.email,
        'Tipo': 'Professore' if current_user.is_professore else 'Studente',
        'ID': current_user.id,
        'Registrato': current_user.created_at.strftime('%d/%m/%Y %H:%M')
    }
    
    # Puoi creare un template HTML o ritornare JSON
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Profilo - Bar Scuola Borsa</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .profile {{ max-width: 600px; margin: 0 auto; }}
            .info-row {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            .label {{ font-weight: bold; display: inline-block; width: 150px; }}
            .btn {{ padding: 10px 20px; margin: 20px 5px; text-decoration: none; 
                   background: #4285f4; color: white; border-radius: 5px; }}
            .btn:hover {{ background: #357ae8; }}
        </style>
    </head>
    <body>
        <div class="profile">
            <h1>Il Tuo Profilo</h1>
            {''.join(f'<div class="info-row"><span class="label">{k}:</span> {v}</div>' 
                     for k, v in info.items())}
            <div style="margin-top: 30px;">
                <a href="{url_for('menu.menu')}" class="btn">Vai al Menu</a>
                <a href="{url_for('auth.logout')}" class="btn" 
                   style="background: #ea4335;">Logout</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


# ============================================
# HELPER FUNCTIONS (opzionali)
# ============================================

def is_professor_email(email):
    """
    Controlla se una email appartiene a un professore
    """
    dominio = os.getenv('DOMINIO_PROFESSORI', 'scuola-borsa.it')
    return email.endswith(f'@{dominio}')


def get_user_discount_type(user):
    """
    Restituisce il tipo di sconto per un utente
    """
    if user and user.is_professore:
        return 'professore'
    return 'normale'