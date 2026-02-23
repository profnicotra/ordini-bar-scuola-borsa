from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from ordiniBarScuolaBorsa.models import get_products, is_bar_open, get_all_positions, add_queue, get_general_notes, Prodotto, db
import json
import logging

logger = logging.getLogger(__name__)
bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.get("/")
def orders():
    """
    Pagina per creare un nuovo ordine.
    Mostra i prezzi corretti in base all'utente autenticato.
    """
    user = current_user if current_user.is_authenticated else None
    posizioni = get_all_positions()
    general_notes = get_general_notes()

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

    return render_template(
        'orders.html',
        positions=posizioni,
        listClass=posizioni,
        general_notes=general_notes,
        user_info=user_info
    )


@bp.route("/new_order", methods=["POST"])
def new_order():
    """
    Crea un nuovo ordine.

    Il frontend manda prodottiSelezionati come JSON array:
        [{"name": "espresso", "price": 1.0, "qty": 2}, ...]

    Qui convertiamo i nomi in prodotto_id cercando nel DB,
    costruiamo le righe nel formato che add_queue si aspetta
    e salviamo l'ordine.
    """
    try:
        # ── 1. Leggi prodotti dal form ──
        selected_products_raw = request.form.get("prodottiSelezionati", "")
        try:
            selected_products = json.loads(selected_products_raw) if selected_products_raw else []
        except Exception as e:
            logger.error(f"Errore parsing prodottiSelezionati: {e}")
            selected_products = []

        if not selected_products:
            logger.warning("Nessun prodotto selezionato.")
            return redirect(url_for('orders.orders'))

        # ── 2. Converti nomi → righe con prodotto_id ──
        user = current_user if current_user.is_authenticated else None
        righe = []

        for item in selected_products:
            nome_prodotto = str(item.get("name", "")).strip()
            qty = max(1, int(item.get("qty", 1)))

            # Cerca il prodotto per nome (case-insensitive)
            prodotto = db.session.query(Prodotto).filter(
                db.func.lower(Prodotto.nome) == nome_prodotto.lower(),
                Prodotto.attivo == True
            ).first()

            if prodotto:
                righe.append({
                    'prodotto_id': prodotto.id,
                    'quantita': qty
                })
            else:
                logger.warning(f"Prodotto non trovato nel DB: '{nome_prodotto}' — riga ignorata")

        if not righe:
            logger.warning("Nessun prodotto valido trovato nel DB.")
            return redirect(url_for('orders.orders'))

        # ── 3. Dati cliente ──
        customer_name    = request.form.get("nome", "").strip()
        customer_surname = request.form.get("cognome", "").strip()

        if user:
            customer_full_name = f"{user.nome} {user.cognome}"
        else:
            customer_full_name = f"{customer_name} {customer_surname}".strip() or "Anonimo"

        # ── 4. Totale ──
        price_raw = request.form.get("total", "0")
        price_clean = price_raw.replace('€', '').replace(',', '.').strip()
        try:
            totale_euro = float(price_clean)
        except ValueError:
            totale_euro = 0.0

        # ── 5. Posizione (classe/tavolo) ──
        position = request.form.get("classe", "").strip()
        positions = get_all_positions()
        position_id = None

        if position:
            # Prima prova come ID numerico diretto
            try:
                position_id = int(position)
            except ValueError:
                # Altrimenti cerca per nome
                pname = position.lower()
                for p in positions:
                    if p.get('nome', '').strip().lower() == pname:
                        position_id = p.get('id')
                        break

        if not position_id:
            logger.warning(f"Posizione non trovata: '{position}'")
            return redirect(url_for('orders.orders'))

        # ── 6. Log ──
        logger.info("--- NUOVO ORDINE ---")
        logger.info(f"Cliente:      {customer_full_name}")
        logger.info(f"Posizione ID: {position_id}")
        logger.info(f"Righe:        {righe}")
        logger.info(f"Totale:       €{totale_euro:.2f}")
        if user:
            logger.info(f"Utente: {user.email} | Professore: {user.is_professor}")

        # ── 7. Salva ordine ──
        success = add_queue(
            posizione_id=position_id,
            righe=righe,
            creato_da=customer_full_name,
            totale_euro=totale_euro,
            stato='NUOVO',
            user=user
        )

        if success:
            logger.info("Ordine salvato correttamente.")
        else:
            logger.error("add_queue ha restituito False.")

    except Exception as e:
        logger.error(f"Errore in new_order: {str(e)}", exc_info=True)
        db.session.rollback()

    return redirect(url_for('menu.menu'))