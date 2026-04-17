<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Scuola Bar Borsa - Red & Black Edition</title>
    <!-- Libreria icone obbligatoria -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com">
    <style>
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: radial-gradient(circle at center, #1a0000 0%, #000000 100%); 
            color: #ffffff; 
            margin: 0; 
            padding: 40px 20px; 
            min-height: 100vh;
        }

        .layout { display: flex; gap: 30px; max-width: 1300px; margin: auto; flex-wrap: wrap; }
        .main-content { flex: 3; min-width: 600px; }

        .header {
            text-align: center;
            padding: 40px;
            background: linear-gradient(145deg, #330000 0%, #000000 100%);
            border: 2px solid #ff0000;
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 0 25px rgba(255, 0, 0, 0.4);
        }

        h1 { color: #ff0000; margin: 0; text-transform: uppercase; letter-spacing: 6px; font-size: 3em; text-shadow: 2px 2px 15px rgba(255, 0, 0, 0.6); }

        table { width: 100%; border-collapse: separate; border-spacing: 0 15px; }
        th { background: #ff0000; color: #000; padding: 18px; text-align: left; text-transform: uppercase; font-size: 0.8em; font-weight: 900; }
        td { background: linear-gradient(90deg, #111 0%, #050505 100%); padding: 15px; border-top: 1px solid #330000; border-bottom: 1px solid #330000; transition: 0.3s; }
        tr:hover td { background: linear-gradient(90deg, #220000 0%, #111 100%); border-color: #ff0000; }

        .nome-prod { font-weight: bold; color: #ff0000; font-size: 1.1em; display: block; }
        .ingr { font-size: 0.8em; color: #bbb; font-style: italic; display: block; }
        .val-margine { color: #ff3333; font-weight: bold; }

        /* BOTTONI AZIONE */
        .btn-cart { background: transparent; border: 2px solid #ff0000; color: #ff0000; padding: 10px; border-radius: 8px; cursor: pointer; transition: 0.3s; }
        .btn-cart:hover { background: #ff0000; color: #000; box-shadow: 0 0 15px #ff0000; }

        .btn-delete { background: transparent; border: none; color: #ff4444; cursor: pointer; font-size: 1.2em; transition: 0.2s; }
        .btn-delete:hover { color: #fff; transform: scale(1.2); }

        /* PANNELLO CARRELLO */
        .cart-panel { 
            flex: 1; min-width: 300px; background: #0a0a0a; border: 2px solid #ff0000; 
            border-radius: 20px; padding: 20px; height: fit-content; position: sticky; top: 20px;
        }
        .cart-title { color: #ff0000; text-transform: uppercase; border-bottom: 1px solid #330000; padding-bottom: 10px; margin-bottom: 15px; }
        #lista-ordine { list-style: none; padding: 0; }
        .item-ordine { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #222; font-size: 0.9em; }
        
        .totale-box { margin-top: 20px; padding: 15px; background: #1a0000; border-radius: 10px; text-align: center; border: 1px solid #ff0000; }
        .totale-box span { color: #ff0000; font-weight: bold; font-size: 1.4em; }

        .badge-cat { border: 1px solid #ff0000; color: #ff0000; padding: 2px 8px; border-radius: 4px; font-size: 0.7em; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>SCUOLA <span style="color:#fff">BAR</span> BORSA</h1>
    </div>

    <div class="layout">
        <div class="main-content">
            <table>
                <thead>
                    <tr>
                        <th>PRODOTTO</th>
                        <th>PREZZO</th>
                        <th>MARGINE</th>
                        <th>CATEGORIA</th>
                        <th>AGGIUNGI</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <span class="nome-prod">Caffè Espresso</span>
                            <span class="ingr">7g Miscela, zucchero</span>
                            <div style="color: #666; font-size: 0.75em; margin-top:5px;">Nota: 3 pezzi di pane</div>
                        </td>
                        <td>1.20 €</td>
                        <td class="val-margine">+1.08 €</td>
                        <td><span class="badge-cat">Caffè</span></td>
                        <td>
                            <button class="btn-cart" onclick="aggiungi('Caffè Espresso', 1.20)">
                                <i class="fas fa-shopping-cart"></i>
                            </button>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <span class="nome-prod">Spremuta Arancia</span>
                            <span class="ingr">3 Arance rosse</span>
                        </td>
                        <td>4.00 €</td>
                        <td class="val-margine">+3.15 €</td>
                        <td><span class="badge-cat">Fresh</span></td>
                        <td>
                            <button class="btn-cart" onclick="aggiungi('Spremuta Arancia', 4.00)">
                                <i class="fas fa-shopping-cart"></i>
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- SEZIONE CARRELLO -->
        <div class="cart-panel">
            <h3 class="cart-title"><i class="fas fa-receipt"></i> IL TUO ORDINE</h3>
            <ul id="lista-ordine">
                <!-- Prodotti dinamici -->
            </ul>
            <div class="totale-box">
                TOTALE: <span id="totale-prezzo">0.00</span> €
            </div>
        </div>
    </div>
</div>

<script>
    let totale = 0;

    function aggiungi(nome, prezzo) {
        const lista = document.getElementById('lista-ordine');
        const li = document.createElement('li');
        li.className = 'item-ordine';
        
        li.innerHTML = `
            <span>${nome} (${prezzo.toFixed(2)}€)</span>
            <button class="btn-delete" onclick="rimuovi(this, ${prezzo})">
                <i class="fas fa-trash-alt"></i>
            </button>
        `;
        
        lista.appendChild(li);
        totale += prezzo;
        aggiornaTotale();
    }

    function rimuovi(btn, prezzo) {
        btn.parentElement.remove();
        totale -= prezzo;
        if (totale < 0) totale = 0;
        aggiornaTotale();
    }

    function aggiornaTotale() {
        document.getElementById('totale-prezzo').innerText = totale.toFixed(2);
    }
</script>

</body>
</html>
