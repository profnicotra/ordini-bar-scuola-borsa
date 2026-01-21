from flask import Blueprint, render_template, jsonify,request
from ordiniBarScuolaBorsa.models import get_queue

bp = Blueprint("queue", __name__, url_prefix="/queue")

@bp.get("/")
def queue():
    data = {"title" : "Coda Bar Scuola Borsa",
        "open": True,   
        "queue" : [get_queue()]},        
    return render_template('queue.html', data=data)

@bp.get("/update", methods=["POST"])
def update_queue():
    dati = request.get_json
    
    return jsonify({"status": "success"})
