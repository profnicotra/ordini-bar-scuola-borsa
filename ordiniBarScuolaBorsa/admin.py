from flask import Blueprint, render_template, jsonify
from ordiniBarScuolaBorsa.models import Prodotto, is_bar_open
from .security import require_operator


bp = Blueprint("admin", __name__, url_prefix="/admin")
bp.before_request(require_operator)

@bp.get("")
@bp.get("/")
def admin():
    prodotti = Prodotto.query.order_by(Prodotto.id).all()
    data = {"title" : "Amministrazione Bar Scuola Borsa",
        "open": is_bar_open(),   
        "items": [
            {
                "id": p.id,
                "nome": p.nome,
                "costo": float(p.costo) if p.costo is not None else None,
                "prezzo": float(p.prezzo_euro) if p.prezzo_euro is not None else None,
                "interni": float(p.prezzo_interni) if p.prezzo_interni is not None else None,
                "categoria": p.categoria,
                "attivo": p.attivo,
            }
            for p in prodotti
        ]}
    return render_template("admin.html", data=data)

@bp.route("/add_product", methods = ["POST"])
def add_product():
    return jsonify(error="La gestione prodotti è in sola consultazione."), 405
