
% rebase('base', title='Display Sala Bar', refresh=5)
<div class="card">
  <div class="title">Coda ordini</div>
  <div>Stato bar: <span class="state" id="state">{{ 'APERTO' if aperto else 'CHIUSO' }}</span></div>
  <form method="post" action="/toggle" style="margin-top:8px">
    <button class="btn">Aperto/Chiuso</button>
  </form>
</div>

% for o in ordini:
  <div class="card">
    <div class="title">#{{o['id']}} • {{o['posizione']}}</div>
    <div class="small">Stato: {{o['stato']}} • {{o['creato_il']}}</div>
    <ul>
      % for r in o['righe']:
        <li></li>
      % end
    </ul>
    <div style="margin-top:8px">
      <form method="post" action="/stato/{{o['id']}}/IN_PREPARAZIONE" style="display:inline"><button class="btn btn3">Prepara</button></form>

    </div>
  </div>
% end
