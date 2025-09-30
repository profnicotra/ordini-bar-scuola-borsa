
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  % if defined('refresh') and refresh:
  <meta http-equiv="refresh" content="{{refresh}}">
  % end
  <title>{{get('title','Bar Scolastico')}}</title>
  <link rel="stylesheet" href="/static/app.css">
  <style>
    body{font-family: system-ui, sans-serif; background:#f8fafc; margin:0;}
    .wrap{max-width:720px;margin:0 auto;padding:16px;}
    .card{background:#fff;border-radius:14px;box-shadow:0 1px 4px rgba(0,0,0,.08);padding:16px;margin:12px 0;}
    .btn{display:inline-block;background:#0ea5e9;color:#fff;border:none;border-radius:10px;padding:10px 14px;font-size:16px}
    .btn:disabled{background:#94a3b8}
    .btn2{background:#16a34a}
    .btn3{background:#f59e0b}
    .btn4{background:#3b82f6}
    .btn5{background:#64748b}
    label{display:block;margin:8px 0 4px;font-size:14px}
    select,input,textarea{width:100%;padding:10px;border:1px solid #cbd5e1;border-radius:10px;font-size:16px}
    .row{display:grid;grid-template-columns:1fr 90px 60px;gap:8px;align-items:end}
    .small{font-size:12px;color:#64748b}
    .title{font-weight:700;font-size:20px;margin:0 0 6px}
    .state{font-weight:700}
    ul{margin:8px 0 0 18px}
  </style>
</head>
<body>
  <div class="wrap">
  % if defined('base'):
    {{!base}}            <!-- per i template che usano rebase('base', ...) -->
  % elif defined('content'):
    {{!content}}         <!-- per le chiamate tipo template('base', content=html) -->
  % end
</div>
</body>
</html>
