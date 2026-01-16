
from flask import Blueprint, render_template

bp = Blueprint("index", __name__)

@bp.get("/")
def index():
    data = {"title" : "Bar Scuola Borsa",
        "open": True,   
        "items" : []}
    
    return render_template('index.html', data=data)

@bp.get("/chi-siamo")
def chi_siamo():
    data = {"title" : "Chi siamo"}
    return render_template('index.html', data=data)

@bp.get("/gallery")
def gallery():
    data = {"title" : "Galleria"}
    return render_template('index.html', data=data)

@bp.get("/contatti")
def contatti():
    data = {"title" : "Contatti"}
    return render_template('index.html', data=data)