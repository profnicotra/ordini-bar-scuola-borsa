from flask import Blueprint, render_template
from ordiniBarScuolaBorsa.models import get_products, is_bar_open
import json
import logging

logger = logging.getLogger(__name__)

bp = Blueprint("menu", __name__, url_prefix="/menu")

@bp.route("/")
@bp.route("")
def menu():
    try:
        prodotti_raw = get_products()  # restituisce lista di DIZIONARI con note_gruppi
        print(prodotti_raw)  # Debug: stampa i dati grezzi
    except Exception as e:
        logger.error(f"Errore get_products(): {e}", exc_info=True)
        prodotti_raw = []

    prodotti_lista = []
    visti = set()  # deduplicazione: ogni prodotto dovrebbe apparire una sola volta

    for p in prodotti_raw:
        try:
            # get_products() ritorna dizionari con chiavi:
            # 'id', 'prodotto', 'prezzo_euro', 'prezzo_interni', 'categoria', 'note_gruppi', ...
            prod_id   = p.get('id')
            nome      = p.get('prodotto', '') or ''
            prezzo    = p.get('prezzo_mostrato', 0) or 0
            categoria = p.get('categoria', '') or ''
            note_gruppi = p.get('note_gruppi', [])

            # Salta se già visto
            if prod_id in visti:
                continue
            visti.add(prod_id)

            prodotti_lista.append({
                "id":           prod_id,
                "prodotto":     str(nome),
                "prezzo_euro":  f"{float(prezzo):.2f}",
                "categoria":    str(categoria).lower().strip(),
                "note_gruppi":  note_gruppi  # Includi i gruppi di note
            })
        except Exception as e:
            logger.warning(f"Errore serializzazione prodotto {p}: {e}")
            continue

    data_json = json.dumps(prodotti_lista, ensure_ascii=False)
    logger.info(f"Menu: {len(prodotti_lista)} prodotti caricati")

    # is_bar_open() ritorna stringa 'true'/'false' oppure None (impostazione non in DB)
    try:
        val = is_bar_open()
        bar_open_val = str(val).lower() if val is not None else "true"
    except Exception as e:
        logger.error(f"Errore is_bar_open(): {e}")
        bar_open_val = "true"

    return render_template(
        'bar.html',
        data_json=data_json,
        bar_open=bar_open_val
    )