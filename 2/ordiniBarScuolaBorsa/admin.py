from flask import Blueprint, render_template, request, redirect
from ordiniBarScuolaBorsa.models import is_bar_open


bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
def admin():
    data = {"title" : "Amministrazione Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items" : []}
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