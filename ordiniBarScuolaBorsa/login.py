from flask import Blueprint, render_template
from ordiniBarScuolaBorsa.models import get_products, is_bar_open

bp = Blueprint("login", __name__, url_prefix="/login")

@bp.get("/")
def login():
    a = get_products()
    print (a)
    data = {"title" : "Menu Bar Scuola Borsa",
            "open": is_bar_open(),   
            "items" : get_products()}
    return render_template('login.html', data=data)
