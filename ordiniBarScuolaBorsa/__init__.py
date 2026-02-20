from flask import Flask
from flask_login import LoginManager
from ordiniBarScuolaBorsa.models import db, User
from dotenv import load_dotenv
import logging
import os

# Carica variabili d'ambiente dal file .env
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Inizializza Flask-Login
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configurazioni
    app.config.from_pyfile("config.py")
    
    # SECRET_KEY per le sessioni (IMPORTANTE!)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chiave-segreta-temporanea-da-cambiare')
    
    # Configurazione Google OAuth
    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # Inizializza il database
    db.init_app(app)
    
    # Inizializza Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect se non autenticato
    login_manager.login_message = 'Effettua il login per continuare'
    login_manager.login_message_category = 'info'
    
    # User loader per Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Importa e registra i blueprint ESISTENTI
    from ordiniBarScuolaBorsa.index import bp as index_bp
    app.register_blueprint(index_bp)

    from ordiniBarScuolaBorsa.menu import bp as menu_bp
    app.register_blueprint(menu_bp)

    from ordiniBarScuolaBorsa.queue_manager import bp as queue_bp
    app.register_blueprint(queue_bp)

    from ordiniBarScuolaBorsa.orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from ordiniBarScuolaBorsa.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from ordiniBarScuolaBorsa.toggle import bp as toggle_bp
    app.register_blueprint(toggle_bp)
    
    # NUOVO: registra il blueprint auth
    from ordiniBarScuolaBorsa.auth import bp as auth_bp, init_oauth
    app.register_blueprint(auth_bp)
    
    # Inizializza OAuth
    init_oauth(app)

    # Crea le tabelle del database
    with app.app_context():
        db.create_all()
        logger.info("Database inizializzato con successo")
        
        # Verifica che la tabella users esista
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        logger.info(f"Tabelle presenti: {tables}")
    
    logger.info("App Flask creata e configurata con successo")
    logger.info(f"Google OAuth configurato: {bool(app.config.get('GOOGLE_CLIENT_ID'))}")

    return app

app = create_app()