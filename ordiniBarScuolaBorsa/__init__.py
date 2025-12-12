from flask import Flask
from ordiniBarScuolaBorsa.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)

    # importa e registra i blueprint
    from ordiniBarScuolaBorsa.index import bp as index_bp
    app.register_blueprint(index_bp)

    # ripeti per gli altri moduli
    from ordiniBarScuolaBorsa.menu import bp as menu_bp
    app.register_blueprint(menu_bp)

    from ordiniBarScuolaBorsa.queue import bp as queue_bp
    app.register_blueprint(queue_bp)

    from ordiniBarScuolaBorsa.orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from ordiniBarScuolaBorsa.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

    return app

app = create_app()