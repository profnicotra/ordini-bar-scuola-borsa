from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from ordiniBarScuolaBorsa.models import get_products, is_bar_open, get_all_positions, add_queue
import json
import logging

logger = logging.getLogger(__name__)
bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.get("/")
def orders():
    """
    Pagina per creare un nuovo ordine
    Mostra i prezzi corretti in base all'utente autenticato
    """
    user = current_user if current_user.is_authenticated else None
    products = get_products(user=user)
    posizioni = get_all_positions()

    user_info = None
    if current_user.is_authenticated:
        user_info = {
            'nome': current_user.nome,
            'cognome': current_user.cognome,
            'email': current_user.email,
            'is_professor': current_user.is_professor,
            'tipo_prezzo': 'Prezzi Riservati' if current_user.is_professor else 'Prezzi Pubblici',
            'picture': current_user.picture
        }

    data = {
        "title": "Nuovo Ordine - Bar Scuola Borsa",
        "open": is_bar_open(),
        "items": [products],
        "classi": posizioni,
        "user_info": user_info
    }

    return render_template('orders.html', data=data, positions=posizioni, listClass=posizioni)


@bp.route("/new_order", methods=["POST"])
def new_order():
    """
    Crea un nuovo ordine
    """
    try:
        # Recupera prodotti selezionati
        selected_products_raw = request.form.get("prodottiSelezionati")
        if selected_products_raw:
            try:
                selectedProducts = json.loads(selected_products_raw)
            except Exception as e:
                logger.error(f"Errore parsing prodotti: {e}")
                selectedProducts = []
        else:
            selectedProducts = []

        general_note = request.form.get("noteGenerali")
        customer_name = request.form.get("nome")
        customer_surname = request.form.get("cognome")

        # Recupera e pulisci il totale
        price_raw = request.form.get("total", "0")
        price = price_raw.replace('€', '').replace(',', '.').strip()
        try:
            totale_euro = float(price)
        except ValueError:
            totale_euro = 0.0

        # Recupera posizione e converti in ID
        position = request.form.get("classe")
        positions = get_all_positions()
        position_id = None

        if position is not None:
            try:
                position_id = int(position)
            except Exception:
                pname = position.strip().lower()
                for p in positions:
                    try:
                        if p.get('nome', '').strip().lower() == pname:
                            position_id = p.get('id')
                            break
                    except Exception:
                        continue

        # Validazione posizione
        if not position_id:
            flash("Seleziona una posizione (tavolo/ufficio)", "error")
            return redirect("/orders")

        # Gestione utente autenticato
        user = current_user if current_user.is_authenticated else None

        if user:
            customer_full_name = f"{user.nome} {user.cognome}"
        else:
            customer_full_name = f"{customer_name} {customer_surname}".strip() if customer_name else "Anonimo"

        # Log debug
        logger.info(f"--- DETTAGLIO ORDINE ---")
        logger.info(f"ID Posizione: {position_id}")
        logger.info(f"Cliente: {customer_full_name}")
        logger.info(f"Prodotti: {selectedProducts}")
        logger.info(f"Totale: €{totale_euro}")
        if user:
            logger.info(f"Utente autenticato: {user.email} (Professore: {user.is_professor})")

        # Crea ordine
        success = add_queue(
            position_id,
            righe="",
            creato_da=customer_full_name,
            totale_euro=totale_euro,
            stato='NUOVO',
            user=user
        )

        if success:
            if user and user.is_professor:
                flash("Ordine creato con successo! Prezzi riservati applicati 👨‍🏫", "success")
            else:
                flash("Ordine creato con successo!", "success")
            logger.info("Ordine creato con successo")
        else:
            flash("Errore nella creazione dell'ordine. Riprova.", "error")
            logger.error("Errore in add_queue")

    except Exception as e:
        logger.error(f"Errore in new_order: {str(e)}", exc_info=True)
        flash("Errore nella creazione dell'ordine. Riprova.", "error")

    return redirect(url_for('menu.menu'))