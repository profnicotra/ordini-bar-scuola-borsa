from ordiniBarScuolaBorsa import app,render_template
import json

@app.route('/orders')
def orders():
    with open("C:\\Users\\24-info-22\\Desktop\\ANNO 25-26\\Linguaggi di programmazione\\ordini-bar-scuola-borsa\\ordiniBarScuolaBorsa\\products.json", "r") as productsJSON:
        data = json.load(productsJSON)
    i = len(data["products"])

    return render_template('orders.html', products = data["products"], prices = data["prices"], available = data["available"], nProducts = i)