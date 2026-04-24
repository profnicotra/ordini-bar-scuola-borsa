from flask import Blueprint, render_template, jsonify, request
from ordiniBarScuolaBorsa.models import get_queue
from ordiniBarScuolaBorsa import models
from ordiniBarScuolaBorsa.models import db, Ordine
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
bp = Blueprint("queue", __name__, url_prefix="/queue")

@bp.get("/")
def queue():
    # Passa la lista di ordini alla template come variabile `queue`.
    data = {"title": "Coda Bar Scuola Borsa", "open": True}
    queue_list = get_queue()
    return render_template('queue.html', queue=queue_list, data=data)

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
        
        # Se lo stato diventa PRONTO, registra il timestamp
        if nuovo_stato == 'PRONTO':
            ordine.stato_pronto_da = datetime.now()
            logger.info(f"Ordine {ordine_id} impostato PRONTO. Timer di 10 minuti attivato.")
        else:
            # Se lo stato cambia da PRONTO a qualcos'altro, resetta il timestamp
            ordine.stato_pronto_da = None
        
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


def check_and_update_ready_orders():
    """Controlla gli ordini PRONTO e li cambia a DA_SPARECCHIARE dopo 10 minuti"""
    try:
        now = datetime.now()
        timeout = now - timedelta(minutes=10)
        
        # Trova ordini che sono stati pronti per più di 10 minuti
        expired_orders = Ordine.query.filter(
            Ordine.stato == 'PRONTO',
            Ordine.stato_pronto_da.isnot(None),
            Ordine.stato_pronto_da <= timeout
        ).all()
        
        if expired_orders:
            logger.info(f"Trovati {len(expired_orders)} ordini scaduti. Cambio stato a DA_SPARECCHIARE")
            for ordine in expired_orders:
                ordine.stato = 'DA_SPARECCHIARE'
                ordine.stato_pronto_da = None
            db.session.commit()
    except Exception as e:
        logger.error(f"Errore nel check_and_update_ready_orders: {str(e)}", exc_info=True)


# @bp.get("/update", methods=["POST"])
# def update_queue():
#     dati = request.get_json
    
#     return jsonify({"status": "success"})
