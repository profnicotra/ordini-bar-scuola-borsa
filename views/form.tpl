
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

      </div>
      % end
    </div>


  </form>
</div>

<script>
  let idx = {{iniziali}};
  function addRow(){
   
  }
</script>
