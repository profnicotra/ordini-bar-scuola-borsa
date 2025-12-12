from flask import Blueprint

bp = Blueprint("queue", __name__, url_prefix="/queue")

@bp.get("/")
def queue():
    return render_template('queue.html')
