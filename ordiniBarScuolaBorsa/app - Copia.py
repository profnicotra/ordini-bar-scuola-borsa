from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Benvenuto sul mio nuovo sito con Flask!"

if __name__ == "__main__":
    app.run(debug=True)
