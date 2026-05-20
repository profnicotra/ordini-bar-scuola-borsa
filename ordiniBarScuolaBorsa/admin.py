from flask import Blueprint, request, jsonify, render_template
import logging

from .models import db, Prodotto, NoteGruppo, Note, get_products, get_general_notes

# Creiamo il Blueprint (il prefisso /admin è gestito da __init__.py)
bp = Blueprint('admin', __name__)

# ==============================================================================
# L'INDIRIZZO SARA': http://localhost:5000/admin/ o /admin
# ==============================================================================
@bp.route('/', strict_slashes=False)
def admin_page():
    try:
        data = {
            'items': get_products(for_admin=True),
            'note_groups': get_general_notes()
        }
    except Exception as e:
        logging.error(f"Errore caricamento dati admin: {e}")
        data = {'items': [], 'note_groups': []}
        
    return render_template('admin.html', data=data)

# ==============================================================================
# GESTIONE PRODOTTI -> /admin/add_product
# ==============================================================================
@bp.route('/add_product', methods=['POST'])
def add_product():
    try:
        data = request.get_json()
        p_id = data.get('id')
        is_attivo = True if data.get('attivo') == 'SI' else False

        if p_id: 
            prodotto = Prodotto.query.get(p_id)
            if not prodotto: return jsonify({'success': False}), 404
            prodotto.nome = data.get('nome')
            prodotto.costo = data.get('costo')
            prodotto.prezzo_euro = data.get('prezzo')
            prodotto.prezzo_interni = data.get('interni')
            prodotto.categoria = data.get('categoria')
            prodotto.attivo = is_attivo
        else: 
            nuovo = Prodotto(
                nome=data.get('nome'), costo=data.get('costo'), 
                prezzo_euro=data.get('prezzo'), prezzo_interni=data.get('interni'),
                categoria=data.get('categoria'), attivo=is_attivo
            )
            db.session.add(nuovo)
            
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Errore Prodotto: {e}")
        return jsonify({'success': False}), 500

@bp.route('/delete_product', methods=['POST'])
def delete_product():
    try:
        prodotto = Prodotto.query.get(request.get_json().get('id'))
        if prodotto:
            db.session.delete(prodotto)
            db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False}), 500

# ==============================================================================
# GESTIONE GRUPPI NOTE -> /admin/add_note_group
# ==============================================================================
@bp.route('/add_note_group', methods=['POST'])
def add_note_group():
    try:
        data = request.get_json()
        g_id = data.get('id')
        
        if g_id: 
            gruppo = NoteGruppo.query.get(g_id)
            if not gruppo: return jsonify({'success': False}), 404
            gruppo.nome = data.get('nome')
            gruppo.esclusivo = data.get('esclusivo')
            gruppo.obbligatorio_default = data.get('obbligatorio')
        else: 
            nuovo = NoteGruppo(
                nome=data.get('nome'), esclusivo=data.get('esclusivo'),
                obbligatorio_default=data.get('obbligatorio')
            )
            db.session.add(nuovo)
            
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Errore Gruppo Note: {e}")
        return jsonify({'success': False}), 500

@bp.route('/delete_note_group', methods=['POST'])
def delete_note_group():
    try:
        gruppo = NoteGruppo.query.get(request.get_json().get('id'))
        if gruppo:
            db.session.delete(gruppo)
            db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False}), 500

# ==============================================================================
# GESTIONE SINGOLE NOTE -> /admin/add_note
# ==============================================================================
@bp.route('/add_note', methods=['POST'])
def add_note():
    try:
        data = request.get_json()
        n_id = data.get('id')
        
        if n_id: 
            nota = Note.query.get(n_id)
            if not nota: return jsonify({'success': False}), 404
            nota.nome = data.get('nome')
            nota.price_delta_euro = data.get('prezzo')
        else: 
            nuova = Note(
                id_gruppo=data.get('id_gruppo'), nome=data.get('nome'),
                price_delta_euro=data.get('prezzo')
            )
            db.session.add(nuova)
            
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        logging.error(f"Errore Singola Nota: {e}")
        return jsonify({'success': False}), 500

@bp.route('/delete_note', methods=['POST'])
def delete_note():
    try:
        nota = Note.query.get(request.get_json().get('id'))
        if nota:
            db.session.delete(nota)
            db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False}), 500