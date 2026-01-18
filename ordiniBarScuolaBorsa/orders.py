from flask import Blueprint, render_template, request, redirect
from ordiniBarScuolaBorsa.models import get_products, is_bar_open

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("/")
def orders():
    data = {"title" : "Menu Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items" : [get_products()]}
    return render_template('orders.html', data = data)

@bp.route("/new_order", methods=["POST"])
def new_order():
    selectedProducts = request.form.get("prodottiSelezionati")
    generalNote = request.form.get("noteGenerali")
    customer_name = request.form.get("nome")
    custumer_surname = request.form.get("cognome")
    position = request.form.get("classe")
    
    print (f"Lista prodotti {selectedProducts}\nNote generale: {generalNote}\nNome cliente: {customer_name}\nCognome cliente: {custumer_surname}\nPosizione {position}")

    return redirect("/orders")