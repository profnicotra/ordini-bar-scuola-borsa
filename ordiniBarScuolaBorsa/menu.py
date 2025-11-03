from ordiniBarScuolaBorsa import app,render_template

@app.route('/menu')
def orders():
    return render_template('menu.html')