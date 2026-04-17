<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Scuola Bar Borsa - Red & Black Edition</title>
    <link rel="stylesheet" href="https://cloudflare.com">
    <style>
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background: radial-gradient(circle at center, #1a0000 0%, #000000 100%); 
            color: #ffffff; 
            margin: 0; 
            padding: 40px 20px; 
        }

        .container { max-width: 1200px; margin: auto; }

        .header {
            text-align: center;
            padding: 30px;
            background: linear-gradient(145deg, #220000 0%, #000000 100%);
            border: 2px solid hsl(223, 92%, 61%);
            border-radius: 20px;
            margin-bottom: 50px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);
        }

        h1 { color: #ff0000; text-transform: uppercase; letter-spacing: 5px; font-size: 2.5em; margin: 0; }
        .sub-header { color: #888; font-size: 0.9em; margin-top: 5px; letter-spacing: 2px; }

        table { width: 100%; border-collapse: separate; border-spacing: 0 15px; }
        
        thead th { 
            color: #ff0000; 
            text-transform: uppercase; 
            padding: 10px; 
            font-size: 0.75em; 
            letter-spacing: 2px;
            text-align: left;
        }

        tr td { 
            background: rgba(15, 15, 15, 0.9);
            padding: 20px; 
            border-top: 1px solid #330000;
            border-bottom: 1px solid #330000;
            transition: 0.3s;
            vertical-align: middle;
        }

        tr:hover td {
            background: #1a0000;
            border-color: #ff0000;
            box-shadow: 0 5px 15px rgba(255, 0, 0, 0.2);
        }

        td:first-child { border-left: 4px solid #ff0000; border-radius: 12px 0 0 12px; }
        td:last-child { border-right: 1px solid #330000; border-radius: 0 12px 12px 0; }

        .nome-prod { font-weight: 900; color: #fff; font-size: 1.2em; display: block; }
        .ingr { color: #777; font-size: 0.8em; font-style: italic; }

        /* Stile Input Note */
        .input-note {
            background: #000;
            border: 1px solid #444;
            color: #ff3333;
            padding: 8px;
            border-radius: 6px;
            font-size: 0.85em;
            width: 100%;
            max-width: 180px;
            outline: none;
        }

        .input-note:focus { border-color: #ff0000; }

        .val-euro { font-family: 'Courier New', monospace; font-size: 0.95em; }
        .val-margine { color: #ff0000; font-weight: 900; font-size: 1.1em; text-shadow: 0 0 5px rgba(255,0,0,0.4); }

        .badge-cat { 
            padding: 3px 10px; 
            border: 1px solid #ff0000; 
            border-radius: 4px; 
            font-size: 0.7em; 
            color: #ff0000; 
            text-transform: uppercase;
        }

        .stato-ok { color: #00ff88; font-weight: bold; font-size: 0.75em; }
        .stato-no { color: #444; font-weight: bold; font-size: 0.75em; text-decoration: line-through; }

    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>SCUOLA <span style="color:#fff">BAR</span> BORSA</h1>
        <div class="sub-header">PROFIT ANALYSIS & NOTES</div>
    </div>

    <table>
        <thead>
            <tr>
                <th>PRODOTTO</th>
                <th>NOTE (EXTRA/TOGLI)</th>
                <th>COSTI</th>
                <th>MARGINE</th>
                <th>CAT.</th>
                <th>STATO</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <span class="nome-prod">Caffè Espresso</span>
                    <span class="ingr">Arabica 100%</span>
                </td>
                <td>
                    <select class="input-note">
                        <option>Senza Schiuma</option>
                        <option>Con Schiuma</option>
                        <option>Macchiato Freddo</option>
                    </select>
                </td>
                <td>
                    <div class="val-euro">C: 0.12 €</div>
                    <div style="color:#ff0000" class="val-euro">P: 1.20 €</div>
                </td>
                <td><span class="val-margine">+1.08 €</span></td>
                <td><span class="badge-cat">Caffè</span></td>
                <td class="stato-ok">DISPONIBILE</td>
            </tr>
            <tr>
                <td>
                    <span class="nome-prod">Toast Classico</span>
                    <span class="ingr">Cotto e Fontina</span>
                </td>
                <td>
                    <input type="text" class="input-note" placeholder="es: togli fontina">
                </td>
                <td>
                    <div class="val-euro">C: 1.20 €</div>
                    <div style="color:#ff0000" class="val-euro">P: 4.50 €</div>
                </td>
                <td><span class="val-margine">+3.30 €</span></td>
                <td><span class="badge-cat">Food</span></td>
                <td class="stato-ok">DISPONIBILE</td>
            </tr>
        </tbody>
    </table>
</div>

</body>
</html>
