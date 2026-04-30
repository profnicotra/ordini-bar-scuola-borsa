from flask import Flask, render_template
import webbrowser

app = Flask(__name__, template_folder='ordiniBarScuolaBorsa/templates')

@app.route('/')
def home():
    return render_template('admin.html')

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:9000')
    app.run(port=9000)
