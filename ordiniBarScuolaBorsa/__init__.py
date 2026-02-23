from flask import Flask
from ordiniBarScuolaBorsa.models import db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)

    # importa e registra i blueprint
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

    with app.app_context():
        db.create_all()
    
    logger.info("App Flask creata e DB inizializzato")

    return app

app = create_app()