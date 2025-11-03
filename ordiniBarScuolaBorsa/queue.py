from ordiniBarScuolaBorsa import app,render_template

@app.route('/queue')
def index():
    return render_template('queue.html')