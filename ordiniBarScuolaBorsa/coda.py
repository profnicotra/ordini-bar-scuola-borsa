from flask import Blueprint, render_template

bp = Blueprint("coda", __name__)

@bp.get("/coda")
def pagina_coda():
    data = {"title": "Monitor Coda - Bar Scuola"}
    return render_template('coda.html', data=data)