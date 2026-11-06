 available_products = []
    seen_products = set()

    for product in get_products(user):
        name = str(product.get('prodotto', '')).strip()
        normalized_name = name.casefold()
        if not name or normalized_name in seen_products:
            continue

        seen_products.add(normalized_name)
        available_products.append({
            'name': name,
            'price': float(product.get('prezzo_mostrato') or 0)
        })

    user_info = None
    if current_user.is_authenticated:
        user_info = {
            'nome':        current_user.nome,
            'cognome':     current_use
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            r.cognome,
            'email':       current_user.email,
            'is_professor': current_user.is_professor,
            'tipo_prezzo': 'Prezzi Riservati' if current_user.is_professor else 'Prezzi Pubblici',
            'picture':     current_user.picture
        }

    # FIX: rimosso "items": [products] — products non era definito qui
    # FIX: rimosso il secondo return render_template duplicato
    return render_template(
        'orders.html',
        positions=posizioni,
        listClass=posizioni,
        general_notes=general_notes,
        user_info=user_info,
        available_products=available_products
    )
