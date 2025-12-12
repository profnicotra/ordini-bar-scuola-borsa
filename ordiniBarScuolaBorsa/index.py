from flask import Blueprint, render_template

bp = Blueprint("index", __name__)

@bp.get("/")
def index():
    return render_template('index.html')