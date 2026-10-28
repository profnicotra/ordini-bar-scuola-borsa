"""Validate a complete order and calculate money from database prices only."""
from decimal import Decimal

from .models import (
    db, is_bar_open, Prodotto, Posizione, Ordine, OrdineRiga, OrdineRigaNota,
)


class OrderError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def positive_id(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise OrderError("Identificativo non valido. Ricarica il menù.")
    if isinstance(value, str) and not value.isascii():
        raise OrderError("Identificativo non valido.")
    if not str(value).isdigit() or int(value) <= 0:
        raise OrderError("Identificativo non valido.")
    return int(value)


def create_order(position_id, items, customer_name, user=None):
    if str(is_bar_open()).lower() == "false":
        raise OrderError("Il bar è chiuso. Non è possibile inviare ordini.", 409)
    if not isinstance(items, list) or not items or len(items) > 100:
        raise OrderError("Seleziona almeno un prodotto valido dal menù.")
    position = db.session.get(Posizione, positive_id(position_id))
    if position is None:
        raise OrderError("Seleziona una classe o un tavolo valido.")
    if not customer_name or len(customer_name) > 200:
        raise OrderError("Inserisci nome e cognome.")

    order = Ordine(
        posizione_id=position.id, user_id=user.id if user else None,
        creato_da=customer_name, stato="NUOVO",
        tipo_prezzo="interni" if user and user.is_professor else "pubblico",
        totale_euro=Decimal("0.00"),
    )
    # Build all rows before adding the order: a bad row rejects the whole cart.
    quantities = {}
    for item in items:
        if not isinstance(item, dict):
            raise OrderError("Il carrello contiene dati non validi. Ricarica il menù.")
        product_id = positive_id(item.get("id"))
        product = db.session.get(Prodotto, product_id)
        if product is None or not product.attivo:
            raise OrderError("Un prodotto non è più disponibile. Ricarica il menù.", 409)
        qty = item.get("qty")
        if type(qty) is not int or not 1 <= qty <= 10:
            raise OrderError("La quantità deve essere un intero tra 1 e 10.")
        quantities[product_id] = quantities.get(product_id, 0) + qty
        if quantities[product_id] > 10:
            raise OrderError("Puoi ordinare al massimo 10 pezzi dello stesso prodotto.")

        selected = item.get("selectedNotes", {})
        if not isinstance(selected, dict):
            raise OrderError("Le varianti selezionate non sono valide.")
        groups = {group.id: group for group in product.note_gruppi}
        normalized = {}
        for key, choices in selected.items():
            group_id = positive_id(key)
            if group_id not in groups or group_id in normalized:
                raise OrderError("Una variante non appartiene al prodotto selezionato.")
            if isinstance(choices, dict):
                choices = [choices]
            if not isinstance(choices, list) or any(not isinstance(n, dict) for n in choices):
                raise OrderError("Le varianti selezionate non sono valide.")
            note_ids = [positive_id(n.get("id")) for n in choices]
            if len(set(note_ids)) != len(note_ids):
                raise OrderError("La stessa variante è stata selezionata più volte.")
            normalized[group_id] = note_ids

        price = product.prezzo_interni if (
            user and user.is_professor and product.prezzo_interni is not None
        ) else product.prezzo_euro
        if price is None or not price.is_finite() or price < 0:
            raise OrderError("Il prezzo del prodotto non è disponibile.", 409)
        notes = []
        for group in groups.values():
            note_ids = normalized.get(group.id, [])
            if group.obbligatorio_default and not note_ids:
                raise OrderError(f"Scegli un'opzione per {group.nome} ({product.nome}).")
            if group.esclusivo and len(note_ids) > 1:
                raise OrderError(f"Scegli una sola opzione per {group.nome}.")
            allowed = {note.id: note for note in group.note}
            for note_id in note_ids:
                if note_id not in allowed:
                    raise OrderError("Una variante non appartiene al gruppo selezionato.")
                note = allowed[note_id]
                notes.append(note)
                price += note.price_delta_euro or Decimal("0.00")
        if not price.is_finite() or price < 0:
            raise OrderError("Il prezzo delle varianti non è valido.", 409)
        price = price.quantize(Decimal("0.01"))
        row = OrdineRiga(prodotto_id=product.id, quantita=qty, prezzo_euro_unit=price)
        row.note_righe = [OrdineRigaNota(nota_id=note.id) for note in notes]
        order.righe.append(row)
        order.totale_euro += price * qty

    db.session.add(order)
    db.session.commit()
    return order
