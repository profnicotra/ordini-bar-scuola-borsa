from flask import Blueprint, render_template, request, redirect
from ordiniBarScuolaBorsa.models import is_bar_open, get_products, db, Prodotto

bp = Blueprint("admin", __name__, url_prefix="/admin")

@bp.get("/")
def admin():
    # Recuperiamo la lista dei prodotti dal database
    prodotti_esistenti = get_products(is_admin=True) 
    
    data = {
        "title" : "Amministrazione Bar Scuola Borsa",
        "open": is_bar_open(),
        "items" : prodotti_esistenti
    }
    return render_template("admin.html", data=data)

@bp.route("/add_product", methods=["POST"])
def add_product():
    # I nomi qui corrispondono esattamente agli attributi 'name' nel form HTML
    product_name = request.form.get("nome_prodotto")
    product_costo = request.form.get("costo")
    product_price = request.form.get("prezzo_euro")
    product_internal_price = request.form.get("prezzo_interni")
    product_margin = request.form.get("margine")
    product_attivo = request.form.get("attivo") == "si"
    product_categoria = request.form.get("categoria")

    nuovo_prodotto = Prodotto(
        nome=product_name,
        costo=product_costo,
        prezzo_euro=product_price,
        prezzo_interni=product_internal_price,
        margine=product_margin,
        attivo=product_attivo,
        categoria=product_categoria
    )

    try:
        db.session.add(nuovo_prodotto)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Errore: {e}")

    return redirect("/admin")