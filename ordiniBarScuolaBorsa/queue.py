from flask import Blueprint, render_template

bp = Blueprint("queue", __name__, url_prefix="/queue")

@bp.get("/")
def queue():
    data = {"title" : "Coda Bar Scuola Borsa",
        "open": True,   
        "items" : []}
    return render_template('queue.html', data=data)
