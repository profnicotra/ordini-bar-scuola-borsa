from ordiniBarScuolaBorsa import app,render_template

@app.route('/menu')
def menu():
    return render_template('menu.html')