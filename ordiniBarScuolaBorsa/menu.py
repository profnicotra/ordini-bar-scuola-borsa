from flask import Blueprint, render_template
from ordiniBarScuolaBorsa.models import get_products

bp = Blueprint("menu", __name__, url_prefix="/menu")

@bp.get("/")
def menu():
    a = get_products()
    print (a)
    data = {"title" : "Menu Bar Scuola Borsa",
            "open": True,   
            "items" : get_products()}
    return render_template('bar.html', data=data)
