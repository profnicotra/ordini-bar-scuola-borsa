from flask import Blueprint, render_template

bp = Blueprint("menu", __name__, url_prefix="/menu")

@bp.get("/")
def menu():
    return render_template('bar.html')