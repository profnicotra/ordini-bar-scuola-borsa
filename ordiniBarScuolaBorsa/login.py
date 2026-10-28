from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint("login", __name__, url_prefix="/login")

@bp.get("")
@bp.get("/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('menu.menu'))
    return render_template('login.html')
