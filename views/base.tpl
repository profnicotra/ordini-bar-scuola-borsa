
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
