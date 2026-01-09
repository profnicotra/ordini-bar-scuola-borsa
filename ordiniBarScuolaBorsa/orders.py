from flask import Blueprint, render_template
from ordiniBarScuolaBorsa import models

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("/")
def orders():
    data = {"title" : "Menu Bar Scuola Borsa",
        "open": True,   
        "items" : [models.get_products()]}
    return render_template('orders.html', data = data)