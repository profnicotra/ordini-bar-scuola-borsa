from flask import Blueprint, render_template
from ordiniBarScuolaBorsa.models import is_bar_open

bp = Blueprint("index", __name__)

@bp.get("/")
def index():
    val = is_bar_open()
    # is_bar_open() ritorna 'true'/'false' (stringa) oppure None
    open_str = str(val).lower() if val is not None else "true"
    data = {
        "title": "Bar Scuola Borsa",
        "open": open_str,
        "items": []
    }
    return render_template('index.html', data=data)

@bp.get("/chi-siamo")
def chi_siamo():
    return render_template('index.html', data={"title": "Chi siamo", "open": "true", "items": []})

@bp.get("/gallery")
def gallery():
    return render_template('index.html', data={"title": "Galleria", "open": "true", "items": []})

@bp.get("/contatti")
def contatti():
    return render_template('index.html', data={"title": "Contatti", "open": "true", "items": []})