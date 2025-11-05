from ordiniBarScuolaBorsa import app,render_template

@app.route('/queue')
def queue():
    return render_template('queue.html')
