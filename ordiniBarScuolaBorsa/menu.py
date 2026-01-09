from ordiniBarScuolaBorsa import app,render_template
import json

@app.route('/menu')
def menu():
    with open ("./menu.json","r") as data:
        productMenu=json.read(data)
    print(productMenu)
    return render_template('menu.html')