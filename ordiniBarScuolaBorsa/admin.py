from flask import Blueprint, render_template, request, jsonify
from .models import (
    db, Prodotto, NoteGruppo, Note,
    toggle_bar_open, is_bar_open, get_products
)


bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.get("/")
def admin():
    # 1. Recupera lo stato (testo 'true' o 'false' per il JS dell'HTML)
    stato_bar = "true" if is_bar_open() else "false"
   
    # 2. Prepara il database per le 3 categorie
    prodotti_db = Prodotto.query.all()
    database_js = {"cibo": [], "bevande": [], "dolci": []}
   
    for p in prodotti_db:
        gruppi_data = []
        # Gestisce i gruppi di note (es. "Salse", "Gusti")
        relazione = getattr(p, 'gruppi', p.note_gruppi)
        for g in relazione:
            note_data = []
            for n in g.note:
                note_data.append({
                    "id": n.id,
                    "nome": n.nome,
                    "disponibile": getattr(n, 'disponibile', True) # Prende il nuovo campo
                })
            gruppi_data.append({"id": g.id, "nome": g.nome, "gusti": note_data})


        # Costruisce l'oggetto prodotto
        prodotto_data = {
            "id": p.id,
            "nome": p.nome,
            "costo": float(p.costo or 0),
            "prezzo": float(p.prezzo_euro or 0),
            "interni": float(p.prezzo_interni or 0),
            "disponibile": p.attivo,
            "gruppi": gruppi_data
        }
       
        # Smista nella categoria corretta
        cat = p.categoria if p.categoria in database_js else "cibo"
        database_js[cat].append(prodotto_data)


    # PASSA I DATI AL TEMPLATE
    return render_template("admin.html", database=database_js, open=stato_bar)




# =====================================================
# GESTIONE STATO BAR
# =====================================================


@bp.post("/toggle_bar")
def admin_toggle_bar():
    """Cambia lo stato di apertura del bar chiamando la funzione in models.py"""
    nuovo_stato = toggle_bar_open()
    return jsonify({"status": "success", "aperto": nuovo_stato})




# =====================================================
# 1. FUNZIONI PRODOTTI
# =====================================================


@bp.post("/aggiungi_prodotto")
def aggiungi_prodotto():
    data = request.json
    try:
        nuovo_p = Prodotto(
            nome=data['nome'].upper(),
            categoria=data.get('categoria', 'cibo'),
            costo=data.get('costo', 0.01),
            prezzo_euro=data.get('prezzo', 0.01),
            prezzo_interni=data.get('interni', 0.01),
            attivo=True
        )
        db.session.add(nuovo_p)
        db.session.commit()
        return jsonify({"status": "success", "id": nuovo_p.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.post("/modifica_prodotto")
def modifica_prodotto():
    data = request.json
    p = Prodotto.query.get_or_404(data['id'])
    campo = data['campo']
    valore = data['valore']
   
    try:
        if campo == 'nome': p.nome = valore.upper()
        elif campo == 'prezzo': p.prezzo_euro = float(valore)
        elif campo == 'costo': p.costo = float(valore)
        elif campo == 'interni': p.prezzo_interni = float(valore)
        elif campo == 'attivo': p.attivo = bool(valore)
       
        # Ricalcolo margine automatico
        p.margine = float(p.prezzo_euro or 0) - float(p.costo or 0)
       
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.post("/elimina_prodotto")
def elimina_prodotto():
    data = request.json
    try:
        p = Prodotto.query.get(data['id'])
        if p:
            db.session.delete(p)
            db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"}), 500




# =====================================================
# 2. FUNZIONI GRUPPI
# =====================================================


@bp.post("/aggiungi_gruppo")
def aggiungi_gruppo():
    data = request.json
    try:
        # id_prodotto è il nome corretto nel tuo models.py
        g = NoteGruppo(nome="NUOVO GRUPPO", id_prodotto=data['prodotto_id'])
        db.session.add(g)
        db.session.commit()
        return jsonify({"status": "success", "id": g.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.post("/modifica_gruppo")
def modifica_gruppo():
    data = request.json
    try:
        g = NoteGruppo.query.get_or_404(data['id'])
        if 'nome' in data: g.nome = data['nome'].upper()
        if 'esclusivo' in data: g.esclusivo = bool(data['esclusivo'])
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"}), 500


@bp.post("/elimina_gruppo")
def elimina_gruppo():
    data = request.json
    try:
        g = NoteGruppo.query.get(data['id'])
        if g:
            db.session.delete(g)
            db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"}), 500




# =====================================================
# 3. FUNZIONI NOTE
# =====================================================


@bp.post("/aggiungi_nota")
def aggiungi_nota():
    data = request.json
    try:
        # id_gruppo è il nome corretto nel tuo models.py
        n = Note(nome="Gusto", id_gruppo=data['gruppo_id'])
        db.session.add(n)
        db.session.commit()
        return jsonify({"status": "success", "id": n.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.post("/modifica_nota")
def modifica_nota():
    data = request.json
    try:
        n = Note.query.get_or_404(data['id'])
        if 'nome' in data: n.nome = data['nome']
        if 'prezzo_extra' in data: n.price_delta_euro = float(data['prezzo_extra'])
        if 'disponibile' in data: n.disponibile = bool(data['disponibile'])
       
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"}), 500


@bp.post("/elimina_nota")
def elimina_nota():
    data = request.json
    try:
        n = Note.query.get(data['id'])
        if n:
            db.session.delete(n)
            db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error"}), 500
