<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Sala Bar - Scuola Borsa Professional</title>
    <style>
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: radial-gradient(circle at center, #1a0000 0%, #000000 100%); 
            color: #ffffff; margin: 0; padding: 20px; min-height: 100vh;
            display: flex; gap: 20px; flex-wrap: wrap;
        }

        .container { flex: 3; min-width: 850px; }
        
        .comanda-box { 
            flex: 1; min-width: 300px; background: rgba(20, 0, 0, 0.95); 
            border: 2px solid #00a6ff; border-radius: 20px; padding: 20px;
            box-shadow: 0 0 20px rgba(0, 166, 255, 0.3); height: fit-content;
            position: sticky; top: 20px;
        }

        .header {
            text-align: center; padding: 20px; background: #000;
            border: 2px solid #00a6ff; border-radius: 20px; margin-bottom: 20px;
        }

        .header h1 { color: #00c8ff; margin: 0; font-size: 2.2em; letter-spacing: 5px; text-shadow: 0 0 10px #00a6ff; }
        .header .sub-title { font-size: 1em; color: #fff; opacity: 0.8; }

        .filter-bar { display: flex; gap: 10px; margin-bottom: 20px; justify-content: center; flex-wrap: wrap; }
        .filter-btn { 
            background: transparent; border: 1px solid #00a6ff; color: #00a6ff; 
            padding: 5px 15px; border-radius: 20px; cursor: pointer; font-size: 0.8em; transition: 0.3s;
        }
        .filter-btn.active { background: #00a6ff; color: #000; box-shadow: 0 0 10px #00a6ff; }

        .btn-blu { 
            background: #00a6ff; border: none; padding: 12px 20px; border-radius: 8px; 
            font-weight: bold; cursor: pointer; color: black; text-transform: uppercase; 
            transition: 0.3s; width: 100%; margin-top: 10px;
        }

        .btn-numerico { background: #ffcc00; color: black; margin-top: 15px; }

        table { width: 100%; border-collapse: separate; border-spacing: 0 8px; }
        th { background: #00aaff; color: #000; padding: 12px; font-size: 0.75em; text-transform: uppercase; text-align: left; }
        
        .info-row td { background: linear-gradient(90deg, #111 0%, #050505 100%); padding: 12px 15px; border-top: 1px solid #00a6ff; cursor: pointer; }
        .info-row:hover td { background: #1a1a1a; }

        .order-item { background: #111; border-left: 4px solid #00a6ff; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .order-top { display: flex; justify-content: space-between; align-items: center; }
        .allergy-text { background: transparent; border: none; border-bottom: 1px solid #444; color: #00ffaa; font-size: 0.8em; width: 100%; outline: none; margin-top: 5px; }
        
        .cat-badge { border: 1px solid #00a6ff; color: #00a6ff; padding: 2px 6px; border-radius: 4px; font-size: 0.7em; text-transform: uppercase; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>SALA BAR</h1>
        <div class="sub-title">Scuola Borsa</div>
    </div>

    <div class="filter-bar" id="filtri"></div>

    <table>
        <thead>
            <tr>
                <th>PRODOTTO</th>
                <th>COSTO</th>
                <th>PREZZO</th>
                <th>INTERNO</th>
                <th>CATEGORIA</th>
                <th>AZIONI</th>
            </tr>
        </thead>
        <tbody id="lista-menu"></tbody>
    </table>
</div>

<div class="comanda-box">
    <h2 style="color:#00a6ff; text-align:center; margin-top:0;">COMANDA</h2>
    <div id="lista-ordine"></div>
    <div id="totale-ordine" style="text-align:right; font-weight:bold; border-top: 2px solid #00a6ff; padding-top:15px; color:#fff; font-size: 1.5em;">0.00 €</div>
    
    <button class="btn-blu btn-numerico" onclick="generaListaNumerica()">ORDINE NUMERICO (1-Z)</button>
    <button class="btn-blu" style="background:#333; color:#fff;" onclick="svuotaComanda()">Svuota Tutto</button>
</div>

<script>
    let totale = 0;
    let prodottiMenu = [
        { n: "Caffè Espresso", c: "Caffetteria", co: 0.15, pr: 1.20, pi: 1.00 },
        { n: "Cappuccino", c: "Caffetteria", co: 0.35, pr: 1.80, pi: 1.50 },
        { n: "Marocchino", c: "Caffetteria", co: 0.30, pr: 1.60, pi: 1.40 },
        { n: "Cornetto Crema", c: "Dolci", co: 0.55, pr: 1.50, pi: 1.30 },
        { n: "Cornetto Choco", c: "Dolci", co: 0.55, pr: 1.50, pi: 1.30 },
        { n: "Panino Crudo", c: "Salato", co: 1.80, pr: 4.50, pi: 4.00 },
        { n: "Pizzetta Sfoglia", c: "Salato", co: 0.60, pr: 2.50, pi: 2.00 },
        { n: "Coca Cola", c: "Bevande", co: 0.60, pr: 2.50, pi: 2.00 },
        { n: "Acqua 50cl", c: "Bevande", co: 0.15, pr: 1.00, pi: 0.80 }
    ];
    let filtroAttuale = "TUTTI";

    function aggiornaInterfaccia() { renderMenu(); renderFiltri(); }

    function renderFiltri() {
        const bar = document.getElementById('filtri');
        const cats = ["TUTTI", ...new Set(prodottiMenu.map(p => p.c.toUpperCase()))];
        bar.innerHTML = cats.map(cat => `
            <button class="filter-btn ${filtroAttuale === cat ? 'active' : ''}" onclick="filtra('${cat}')">${cat}</button>
        `).join('');
    }

    function filtra(cat) { filtroAttuale = cat; renderMenu(); renderFiltri(); }

    function renderMenu() {
        const corpo = document.getElementById('lista-menu');
        corpo.innerHTML = "";
        prodottiMenu.forEach((p, index) => {
            if (filtroAttuale !== "TUTTI" && p.c.toUpperCase() !== filtroAttuale) return;
            const riga = document.createElement('tr');
            riga.className = "info-row";
            riga.onclick = () => ordina(p.n, p.pr);
            riga.innerHTML = `
                <td><b style="color:#00c8ff">${p.n}</b></td>
                <td style="color:#777">${p.co.toFixed(2)}€</td>
                <td style="font-weight:bold">${p.pr.toFixed(2)}€</td>
                <td style="color:#00a6ff">${p.pi.toFixed(2)}€</td>
                <td><span class="cat-badge">${p.c}</span></td>
                <td><button style="color:#ff4444; background:none; border:1px solid #ff4444; padding:4px 8px; border-radius:5px; cursor:pointer" onclick="event.stopPropagation(); eliminaProdotto(${index})">🗑️</button></td>
            `;
            corpo.appendChild(riga);
        });
    }

    function eliminaProdotto(index) { prodottiMenu.splice(index, 1); aggiornaInterfaccia(); }

    function ordina(nome, prezzo) {
        const lista = document.getElementById('lista-ordine');
        const id = 'ord-' + Date.now();
        const voce = document.createElement('div');
        voce.className = "order-item";
        voce.id = id;
        voce.innerHTML = `
            <div class="order-top">
                <span class="nome-prod-comanda">${nome}</span><b>${prezzo.toFixed(2)}€</b>
                <button style="color:#ff4444; border:none; background:none; cursor:pointer" onclick="rimuoviDallOrdine('${id}', ${prezzo})">✕</button>
            </div>
            <input type="text" class="allergy-text" placeholder="Note...">
        `;
        lista.appendChild(voce);
        aggiornaCassa(prezzo);
    }

    function generaListaNumerica() {
        const items = document.querySelectorAll('.order-item');
        if (items.length === 0) return alert("Comanda vuota!");
        let lista = [];
        items.forEach(item => {
            lista.push({ nome: item.querySelector('.nome-prod-comanda').innerText, note: item.querySelector('.allergy-text').value });
        });
        lista.sort((a, b) => a.nome.localeCompare(b.nome));
        let messaggio = "LISTA PRODUZIONE (1 -> Z):\n\n";
        lista.forEach((p, index) => {
            messaggio += `${index + 1}. ${p.nome.toUpperCase()} ${p.note ? '['+p.note+']' : ''}\n`;
        });
        alert(messaggio);
    }

    function rimuoviDallOrdine(id, pr) { document.getElementById(id).remove(); aggiornaCassa(-pr); }
    function aggiornaCassa(v) { totale += v; document.getElementById('totale-ordine').innerText = Math.abs(totale).toFixed(2) + " €"; }
    function svuotaComanda() { document.getElementById('lista-ordine').innerHTML = ""; totale = 0; aggiornaCassa(0); }
    
    window.onload = aggiornaInterfaccia;
</script>
</body>
</html>
