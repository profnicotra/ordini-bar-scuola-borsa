<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Tabella Progetto Scuola</title>
    <style>
        /* Stile per rendere la tabella più bella */
        table {
            width: 100%;
            border-collapse: collapse; /* Rimuove lo spazio tra i bordi */
            font-family: Arial, sans-serif;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50; /* Colore verde per l'intestazione */
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2; /* Colore alternato per le righe */
        }
        tr:hover {
            background-color: #ddd; /* Effetto al passaggio del mouse */
        }
    </style>
</head>
<body>

    <h2>Tabella Riassuntiva del Progetto</h2>

    <table>
        <thead>
            <tr>
                <th>Materia</th>
                <th>Argomento</th>
                <th>Stato</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Informatica</td>
                <td>Tag HTML e Tabelle</td>
                <td>Completato</td>
            </tr>
            <tr>
                <td>Storia</td>
                <td>La Rivoluzione Industriale</td>
                <td>In corso</td>
            </tr>
            <tr>
                <td>Scienze</td>
                <td>Il Sistema Solare</td>
                <td>Da iniziare</td>
            </tr>
        </tbody>
    </table>

</body>
</html>
