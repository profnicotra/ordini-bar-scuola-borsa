from flask import Blueprint, render_template, request, redirect
from ordiniBarScuolaBorsa.models import get_products, is_bar_open, get_all_positions, add_queue
import json

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("/")
def orders():
    # Recupera la lista di dizionari dal DB: [{'id': 1, 'nome': 'banco bar'}, ...]
    posizioni = get_all_positions()
    
    data = {
        "title": "Menu Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items": [get_products()],
        "classi": posizioni  # Questa variabile contiene ora tutti i tuoi tavoli/uffici/classi
    }
    positions = get_all_positions()
    listClass = get_all_positions()
    # print(listClass)
    
    return render_template('orders.html', data=data, positions=positions, listClass=listClass)

@bp.route("/new_order", methods=["POST"])
def new_order():
    selected_products_raw = request.form.get("prodottiSelezionati")
    if selected_products_raw:
        try:
            selectedProducts = json.loads(selected_products_raw)
        except Exception as e:
            selectedProducts = selected_products_raw
    else:
        selectedProducts = []

    generalNote = request.form.get("noteGenerali")
    customer_name = request.form.get("nome")
    customer_surname = request.form.get("cognome")
    price_raw = request.form.get("total")
    price = price_raw.replace('€', '').replace(',', '.').strip()

    
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

    return redirect("/orders")