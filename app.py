from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"Id: {self.id}, Name: {self.name}"

@app.route('/')
def index():
    products = Product.query.filter_by(active=True).all()
    return render_template("home.html", products=products)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)