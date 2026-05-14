from flask import Blueprint, render_template, request, redirect, jsonify
# Importa i modelli necessari
from ordiniBarScuolaBorsa.models import is_bar_open, get_products, get_general_notes, db, Prodotto, NoteGruppo, Note

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
def admin():
    # Recuperiamo Prodotti e Gruppi Note REALI dal database
    prodotti_scuola = get_products(for_admin=True) 
    note_gruppi_scuola = get_general_notes()
    
    data = {
        "title" : "Amministrazione Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items" : prodotti_scuola,
        "note_groups" : note_gruppi_scuola
    }
    return render_template("admin.html", data=data)

# ==========================================
# ROTTE PRODOTTI
# ==========================================
@bp.route("/add_product", methods=["POST"])
def add_product():
    dati = request.get_json()
    p_id = dati.get("id")
    nome = dati.get("nome")
    costo = dati.get("costo")
    prezzo = dati.get("prezzo")
    interni = dati.get("interni")
    categoria = dati.get("categoria")
    attivo = True if dati.get("attivo") == "SI" else False

    if p_id:
        prodotto = Prodotto.query.get(p_id)
        if prodotto:
            prodotto.nome = nome
            prodotto.costo = costo
            prodotto.prezzo_euro = prezzo
            prodotto.prezzo_interni = interni
            prodotto.categoria = categoria
            prodotto.attivo = attivo
    else:
        prodotto = Prodotto(nome=nome, costo=costo, prezzo_euro=prezzo, prezzo_interni=interni, categoria=categoria, attivo=attivo)
        db.session.add(prodotto)
        
    db.session.commit()
    return jsonify({"success": True})

@bp.route("/delete_product", methods=["POST"])
def delete_product():
    dati = request.get_json()
    prodotto = Prodotto.query.get(dati.get("id"))
    if prodotto:
        db.session.delete(prodotto)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

# ==========================================
# ROTTE GRUPPI NOTE
# ==========================================
@bp.route("/add_note_group", methods=["POST"])
def add_note_group():
    dati = request.get_json()
    g_id = dati.get("id")
    nome = dati.get("nome")
    esclusivo = dati.get("esclusivo")
    obbligatorio = dati.get("obbligatorio")

    if g_id: # Modifica
        gruppo = NoteGruppo.query.get(g_id)
        if gruppo:
            gruppo.nome = nome
            gruppo.esclusivo = esclusivo
            gruppo.obbligatorio_default = obbligatorio
    else: # Inserimento
        gruppo = NoteGruppo(nome=nome, esclusivo=esclusivo, obbligatorio_default=obbligatorio)
        db.session.add(gruppo)
        
    db.session.commit()
    return jsonify({"success": True})

@bp.route("/delete_note_group", methods=["POST"])
def delete_note_group():
    dati = request.get_json()
    gruppo = NoteGruppo.query.get(dati.get("id"))
    if gruppo:
        # Eliminiamo prima le note collegate per evitare errori di chiave esterna
        Note.query.filter_by(id_gruppo=gruppo.id).delete()
        db.session.delete(gruppo)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})

# ==========================================
# ROTTE SINGOLE NOTE    
# ==========================================
@bp.route("/add_note", methods=["POST"])
def add_note():
    dati = request.get_json()
    n_id = dati.get("id")
    id_gruppo = dati.get("id_gruppo")
    nome = dati.get("nome")
    prezzo = dati.get("prezzo")

    if n_id: # Modifica
        nota = Note.query.get(n_id)
        if nota:
            nota.nome = nome
            nota.price_delta_euro = prezzo
    else: # Inserimento
        nota = Note(id_gruppo=id_gruppo, nome=nome, price_delta_euro=prezzo)
        db.session.add(nota)
        
    db.session.commit()
    return jsonify({"success": True})

@bp.route("/delete_note", methods=["POST"])
def delete_note():
    dati = request.get_json()
    nota = Note.query.get(dati.get("id"))
    if nota:
        db.session.delete(nota)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False})