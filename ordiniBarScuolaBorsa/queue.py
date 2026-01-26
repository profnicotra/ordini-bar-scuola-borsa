from flask import Blueprint, render_template, jsonify,request
from ordiniBarScuolaBorsa.models import get_queue, jsonify, request
from ordiniBarScuolaBorsa import models
from ordiniBarScuolaBorsa.models import db, Ordine
import logging

logger = logging.getLogger(__name__)
bp = Blueprint("queue", __name__, url_prefix="/queue")

@bp.get("/")
def queue():
    data = {"title" : "Coda Bar Scuola Borsa",
        "open": True,   
        "queue" : [get_queue()]},        
    return render_template('queue.html', data=data)

@bp.get("/api/ordini")
def get_ordini():
    """Recupera tutti gli ordini dalla coda"""
    try:
        logger.info("GET /queue/api/ordini - Caricamento ordini")
        ordini = models.get_queue()
        logger.info(f"GET /queue/api/ordini - Caricati {len(ordini)} ordini")
        return jsonify(ordini), 200
    except Exception as e:
        logger.error(f"Errore in get_ordini: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@bp.post("/api/ordini/<int:ordine_id>/stato")
def update_ordine_stato(ordine_id):
    """Aggiorna lo stato di un ordine"""
    try:
        data = request.get_json()
        nuovo_stato = data.get('stato')
        
        ordine = Ordine.query.get(ordine_id)
        if not ordine:
            return jsonify({"error": "Ordine non trovato"}), 404
        
        ordine.stato = nuovo_stato
        db.session.commit()
        
        return jsonify({"success": True, "stato": nuovo_stato}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.delete("/api/ordini/<int:ordine_id>")
def delete_ordine(ordine_id):
    """Elimina un ordine"""
    try:
        ordine = Ordine.query.get(ordine_id)
        if not ordine:
            return jsonify({"error": "Ordine non trovato"}), 404
        
        db.session.delete(ordine)
        db.session.commit()
        
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.get("/update", methods=["POST"])
def update_queue():
    dati = request.get_json
# @bp.get("/update", methods=["POST"])
# def update_queue():
#     dati = request.get_json
    
#     return jsonify({"status": "success"})
