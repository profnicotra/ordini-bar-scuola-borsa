from flask import Blueprint, render_template, redirect
from ordiniBarScuolaBorsa.models import toggle_bar_open, is_bar_open

bp = Blueprint("toggle", __name__, url_prefix="/toggle")

@bp.get("/")
def toggle():
    data = {
        "title" : "Apri e Chiudi Bar Scuola Borsa",
        "open": is_bar_open()
    }

    return render_template('toggle.html', data=data)

@bp.route("/changeBarStatus", methods=["POST"])
def changeBarStatus():
    toggle_bar_open()
    return redirect("/toggle")