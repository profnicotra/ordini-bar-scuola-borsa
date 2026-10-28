"""Access control for bar operators and request forgery protection."""
import secrets

from flask import current_app, jsonify, redirect, request, session, url_for
from flask_login import current_user


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def valid_csrf():
    token = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    return bool(expected and token and secrets.compare_digest(expected.encode(), token.encode()))


def require_operator():
    if current_app.config.get("REQUIRE_OPERATOR_LOGIN", True):
        if not current_user.is_authenticated:
            if "/api/" in request.path or request.method != "GET":
                return jsonify(error="Accedi con Google per continuare."), 401
            return redirect(url_for("login.login"))
        if current_user.email.lower() not in current_app.config["ADMIN_EMAILS"]:
            return jsonify(error="Questo account non è autorizzato a gestire il bar."), 403
    if request.method not in {"GET", "HEAD", "OPTIONS"} and not valid_csrf():
        return jsonify(error="Sessione scaduta. Ricarica la pagina e riprova."), 400
