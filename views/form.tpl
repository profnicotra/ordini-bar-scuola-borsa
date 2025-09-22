
% rebase('base', title='Nuovo Ordine', refresh=None)
<div class="card">
  <div class="title">Bar scolastico</div>
  <div>Stato bar: <span class="state">{{ 'APERTO' if aperto else 'CHIUSO' }}</span></div>
</div>

<div class="card">
  <form method="post" action="/ordina">
    <label>Posizione attuale (aula)</label>
    <select name="posizione_id" required>
      % for p in posizioni:
        <option value="{{p['id']}}">{{p['nome']}}</option>
      % end
    </select>

    <label>Il tuo nome (docente)</label>
    <input name="creato_da" placeholder="Es. Rossi" required>

    <div id="righe">
      % for i in range(1, iniziali+1):
      <div class="row">
        <select name="prodotto_id_{{i}}">
          % for pr in prodotti:
            <option value="{{pr['id']}}">{{pr['nome']}}</option>
          % end
        </select>
        <input type="number" name="quantita_{{i}}" value="1" min="1">
        <input type="text" name="nota_{{i}}" placeholder="Nota">
      </div>
      % end
    </div>

    <div class="small">(Puoi aggiungere righe con il pulsante qui sotto)</div>
    <button type="button" class="btn btn5" onclick="addRow()">+ Aggiungi prodotto</button>
    <br><br>
    <button class="btn btn2" {{'disabled' if not aperto else ''}}>Invia ordine</button>
  </form>
</div>

<script>
  let idx = {{iniziali}};
  function addRow(){
    idx += 1;
    const r = document.createElement('div');
    r.className = 'row';
    r.innerHTML = `
      <select name="prodotto_id_${idx}">
        ${[
% for pr in prodotti:
          `<option value="{{pr['id']}}">{{pr['nome']}}</option>`,
% end
        ].join('')}
      </select>
      <input type="number" name="quantita_${idx}" value="1" min="1">
      <input type="text" name="nota_${idx}" placeholder="Nota">
    `;
    document.getElementById('righe').appendChild(r);
  }
</script>
