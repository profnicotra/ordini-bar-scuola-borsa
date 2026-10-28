from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
import json
import logging

from .models import db, get_all_positions, get_general_notes, get_products
from .order_service import create_order, OrderError
from .security import valid_csrf

logger = logging.getLogger(__name__)
bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.get("/")
def orders():
    user = current_user if current_user.is_authenticated else None
    return render_template(
        "orders.html", listClass=get_all_positions(),
        general_notes=get_general_notes(), catalog=get_products(user),
        user_info={"nome": user.nome or "", "cognome": user.cognome or ""} if user else None,
    )


@bp.post("/new_order")
def new_order():
    if not valid_csrf():
        return jsonify(error="Sessione scaduta. Ricarica la pagina e riprova."), 400
    try:
        try:
            items = json.loads(request.form.get("prodottiSelezionati", ""))
        except (ValueError, TypeError):
            raise OrderError("Il carrello non è valido. Ricarica il menù.")
        user = current_user if current_user.is_authenticated else None
        if user:
            customer_name = " ".join(filter(None, [user.nome, user.cognome])) or user.email
        else:
            names = [request.form.get(field, "").strip() for field in ("nome", "cognome")]
            if any(not 2 <= len(name) <= 100 or not any(c.isalpha() for c in name)
                   or not all(c.isalpha() or c in " '-’" for c in name) for name in names):
                raise OrderError("Inserisci nome e cognome validi.")
            customer_name = " ".join(names)
        order = create_order(request.form.get("classe"), items, customer_name, user)
        return jsonify(success=True, order_id=order.id, totale_euro=float(order.totale_euro)), 201
    except OrderError as error:
        db.session.rollback()
        return jsonify(error=str(error)), error.status
    except Exception:
        db.session.rollback()
        logger.exception("Impossibile salvare l'ordine")
        return jsonify(error="Ordine non salvato. Riprova tra poco."), 500
