from flask import Flask
from ordiniBarScuolaBorsa.models import db
from flask_login import LoginManager
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Carica la configurazione dal file config.py nella stessa directory
    config_path = os.path.join(os.path.dirname(__file__), 'config.py')
    app.config.from_pyfile(config_path)

    db.init_app(app)
    login_manager.init_app(app)

    # Importa e registra i blueprint
    from ordiniBarScuolaBorsa.index import bp as index_bp
    app.register_blueprint(index_bp)

    from ordiniBarScuolaBorsa.menu import bp as menu_bp
    app.register_blueprint(menu_bp)

    from ordiniBarScuolaBorsa.queue import bp as queue_bp
    app.register_blueprint(queue_bp)

    from ordiniBarScuolaBorsa.orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from ordiniBarScuolaBorsa.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from ordiniBarScuolaBorsa.toggle import bp as toggle_bp
    app.register_blueprint(toggle_bp)

    from ordiniBarScuolaBorsa.login import bp as login_bp
    app.register_blueprint(login_bp)

    from ordiniBarScuolaBorsa.auth import bp as auth_bp, init_oauth
    app.register_blueprint(auth_bp)

    # Inizializza OAuth solo se le credenziali Google sono configurate
    if app.config.get('GOOGLE_CLIENT_ID') and app.config.get('GOOGLE_CLIENT_SECRET'):
        init_oauth(app)
        logger.info("Google OAuth inizializzato")
    else:
        logger.warning("GOOGLE_CLIENT_ID/SECRET non configurati — OAuth Google disabilitato")

    # user_loader: dice a flask_login come ricaricare l'utente dalla sessione
    from ordiniBarScuolaBorsa.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    logger.info("App Flask creata e DB inizializzato")
    return app

app = create_app()