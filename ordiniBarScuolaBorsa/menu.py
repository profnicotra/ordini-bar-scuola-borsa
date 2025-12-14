from flask import Blueprint, render_template

bp = Blueprint("menu", __name__, url_prefix="/menu")

@bp.get("/")
def menu():
    data = {"title" : "Menu Bar Scuola Borsa",
            "open": True,   
            "items" : []}
    return render_template('bar.html', data=data)