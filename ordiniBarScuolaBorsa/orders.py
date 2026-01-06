from flask import Blueprint, render_template
from ordiniBarScuolaBorsa import models

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("/")
def orders():
    data = models.get_products()
    return render_template('orders.html', product = data)