<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for
=======
from flask import Blueprint, render_template, request, redirect, flash
from flask_login import current_user
>>>>>>> bea788e191f816616f53a5b9769625bea6d0796c
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
    # Recupera i prodotti con i prezzi corretti per l'utente
    user = current_user if current_user.is_authenticated else None
    products = get_products(user=user)
    
    # Recupera le posizioni (tavoli, uffici, classi)
    posizioni = get_all_positions()
    
    # Informazioni utente per il template
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
        "items": [products],  # Mantiene compatibilità con template esistente
        "classi": posizioni,
        "user_info": user_info
    }
    
    positions = posizioni  # Alias per compatibilità
    listClass = posizioni  # Alias per compatibilità
    
    return render_template('orders.html', data=data, positions=positions, listClass=listClass)

@bp.route("/new_order", methods=["POST"])
def new_order():
    """
    Crea un nuovo ordine
    MANTIENE la logica esistente + aggiunge supporto autenticazione
    """
    try:
        # === RECUPERA DATI DAL FORM (LOGICA ESISTENTE) ===
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
        
        # Recupera il totale dal form (logica esistente)
        price_raw = request.form.get("total", "0")
        # Pulisci il formato del prezzo
        price = price_raw.replace('€', '').replace(',', '.').strip()
        try:
            totale_euro = float(price)
        except ValueError:
            totale_euro = 0.0
        
        # Recupera posizione
        position = request.form.get("classe")
        
        # === CONVERTI POSIZIONE IN ID (LOGICA ESISTENTE) ===
        positions = get_all_positions()
        position_id = None
        
        if position is not None:
            # Prova a interpretarlo come intero (ID già passato)
            try:
                position_id = int(position)
            except Exception:
                # Cerca per nome (case-insensitive, strip)
                pname = position.strip().lower()
                for p in positions:
                    try:
                        if p.get('nome', '').strip().lower() == pname:
                            position_id = p.get('id')
                            break
                    except Exception:
                        continue
        
        # === VALIDAZIONE ===
        if not position_id:
            flash("Seleziona una posizione (tavolo/ufficio)", "error")
            return redirect("/orders")
        
        # === GESTIONE UTENTE (NUOVO) ===
        user = current_user if current_user.is_authenticated else None
        
        # Nome cliente: usa utente autenticato se disponibile, altrimenti usa form
        if user:
            customer_full_name = f"{user.nome} {user.cognome}"
        else:
            customer_full_name = f"{customer_name} {customer_surname}" if customer_name else "Anonimo"
        
        # === LOG DEBUG (LOGICA ESISTENTE) ===
        logger.info(f"--- DETTAGLI ORDINE ---")
        logger.info(f"ID Posizione/Tavolo: {position_id}")
        logger.info(f"Cliente: {customer_full_name}")
        logger.info(f"Prodotti: {selectedProducts}")
        logger.info(f"Totale: €{totale_euro}")
        if user:
            logger.info(f"Utente autenticato: {user.email} (Professore: {user.is_professor})")
        
        # === CREA ORDINE (COMPATIBILE CON LOGICA ESISTENTE + NUOVO) ===
        success = add_queue(
            position_id,
            righe="",  # Mantiene compatibilità (il tuo codice non usa righe qui)
            creato_da=customer_full_name,
            totale_euro=totale_euro,
            stato='NUOVO',
            user=user  # NUOVO: passa utente se autenticato
        )

        print(position_id, customer_full_name, totale_euro, user)
        
        if success:
            # Messaggio di conferma personalizzato
            if user and user.is_professor:
                flash(f"Ordine creato con successo! Prezzi riservati applicati 👨‍🏫", "success")
            else:
                flash("Ordine creato con successo!", "success")
            
            logger.info(f"Ordine creato con successo")
        else:
            flash("Errore nella creazione dell'ordine. Riprova.", "error")
            logger.error("Errore in add_queue")
        
    except Exception as e:
        logger.error(f"Errore in new_order: {str(e)}", exc_info=True)
        flash("Errore nella creazione dell'ordine. Riprova.", "error")
    
<<<<<<< HEAD
    # Questo cattura l'ID (es: "35" per 1D, "1" per banco bar)
    # Il form può inviare l'`id` oppure il `nome` della classe/tavolo.
    position = request.form.get("classe")

    # Se è arrivato il nome, convertirlo nell'id corrispondente
    positions = get_all_positions()
    position_id = None
    if position is not None:
        # prova a interpretarlo come intero (id già passato)
        try:
            position_id = int(position)
        except Exception:
            # cerca per nome (case-insensitive, strip)
            pname = position.strip().lower()
            for p in positions:
                try:
                    if p.get('nome', '').strip().lower() == pname:
                        position_id = p.get('id')
                        break
                except Exception:
                    continue
    # usa `position_id` (può essere None se non trovata)
    position = position_id
    
    # Log di verifica
    print(f"--- DETTAGLI ORDINE ---")
    print(f"ID Posizione/Tavolo: {position}") 
    print(f"Cliente: {customer_name} {customer_surname}")
    print(f"Prodotti: {selectedProducts}")
    customer_full_name = f"{customer_name} {customer_surname}"
    print(price)

    add_queue(position, righe="", creato_da=customer_full_name, totale_euro= price)

    return redirect(url_for('menu.menu'))
=======
    return redirect("/orders")
>>>>>>> bea788e191f816616f53a5b9769625bea6d0796c
