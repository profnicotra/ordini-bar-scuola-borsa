from flask import Blueprint, render_template, request, redirect
from ordiniBarScuolaBorsa.models import db, Prodotto, is_bar_open

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
def admin():
    # Recuperiamo tutti i prodotti veri dal database
    prodotti = Prodotto.query.all()
    
    items = []
    for p in prodotti:
        # Costruiamo l'oggetto delle varianti/note per il tuo JS
        varianti = {}
        for gruppo in p.note_gruppi:
            varianti[gruppo.nome] = [nota.nome for nota in gruppo.note]
            
        # Creiamo il dizionario usando le tue identiche chiavi Javascript
        items.append({
            "id": p.id,
            "n": p.nome,
            "c": str(p.costo) if p.costo else "0",
            "p": str(p.prezzo_euro) if p.prezzo_euro else "0",
            "i": str(p.prezzo_interni) if p.prezzo_interni else "0",
            "m": str(p.margine) if p.margine else "0",
            "a": "si" if p.attivo else "no",
            "g": p.categoria or "-",
            "v": varianti
        })
    
    data = {
        "title" : "Amministrazione Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items" : items
    }
    
    return render_template("admin.html", data=data)

@bp.route("/add_product", methods = ["POST"])
def add_product():
    product_id = request.form.get("id")
    product_name = request.form.get("nome_prodotto")
    product_price = request.form.get("prezzo")
    product_margin = request.form.get("margine")
    product_internal_price = request.form.get("prezzo_interno")

    print (f"ID: {product_id}\nNome: {product_name}\nPrezzo: {product_price}\nMargine: {product_margin}\nPrezzo interno {product_internal_price}")
    return redirect("/admin")