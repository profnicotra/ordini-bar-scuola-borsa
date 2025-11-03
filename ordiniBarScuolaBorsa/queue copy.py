from ordiniBarScuolaBorsa import app,render_template

@app.route('/admin')
def index():
    return render_template('admin.html')