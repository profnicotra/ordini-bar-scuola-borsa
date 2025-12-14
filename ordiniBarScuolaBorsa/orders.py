from flask import Blueprint, render_template

bp = Blueprint("orders", __name__, url_prefix="/orders")

@bp.get("/")
def orders():
    # with open("C:\\Users\\24-info-22\\Desktop\\ANNO 25-26\\Linguaggi di programmazione\\ordini-bar-scuola-borsa\\ordiniBarScuolaBorsa\\products.json", "r") as productsJSON:
    #     data = json.load(productsJSON)
    # i = len(data["products"])
    data = {"title" : "Ordini Bar Scuola Borsa",
        "open": True,   
        "items" : []}
    return render_template('orders.html')
    #return render_template('orders.html', products = data["products"], prices = data["prices"], available = data["available"], nProducts = i)