from flask import Blueprint, render_template

bp = Blueprint("toggle", __name__, url_prefix="/toggle")

@bp.get("/")
def index():
    
    data = {"title" : "Apri e Chiudi Bar Scuola Borsa",
        "open": True,   
        "items" : []}
    return render_template('toggle.html', data=data)