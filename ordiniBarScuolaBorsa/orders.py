from flask import Blueprint, render_template, request, redirect
from ordiniBarScuolaBorsa.models import get_products, is_bar_open
import json

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("/")
def orders():
    data = {"title" : "Menu Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items" : [get_products()]}
    return render_template('orders.html', data = data)

@bp.route("/new_order", methods=["POST"])
def new_order():
    # riceve la stringa JSON inviata dall'input hidden prodottiSelezionati
    selected_products_raw = request.form.get("prodottiSelezionati")
    if selected_products_raw:
        try:
            selectedProducts = json.loads(selected_products_raw)
        except Exception as e:
            # fallback: tenere la stringa grezza in caso di errore di parsing
            selectedProducts = selected_products_raw
    else:
        selectedProducts = []

    generalNote = request.form.get("noteGenerali")
    customer_name = request.form.get("nome")
    custumer_surname = request.form.get("cognome")
    position = request.form.get("classe")
    
    # qui puoi processare/salvare i dati come preferisci (db, file, invio API, ecc.)
    print (f"Lista prodotti: {selectedProducts}\nNote generale: {generalNote}\nNome cliente: {customer_name}\nCognome cliente: {custumer_surname}\nPosizione: {position}")

    return redirect("/orders")