
from flask import Blueprint, render_template

bp = Blueprint("index", __name__)

@bp.get("/")
def index():
    data = {"title" : "Bar Scuola Borsa",
        "open": True,   
        "items" : []}
    
    return render_template('index.html', data=data)