from ordiniBarScuolaBorsa import app,render_template

@app.route('/orders')
def orders():
    return render_template('orders.html')