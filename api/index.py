# api/index.py
from flask import Flask, jsonify, Response
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return Response("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Flashcards</title>
  <style>
    body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#0f172a;color:#e2e8f0}
    header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;border-bottom:1px solid #1f2937;background:#111827}
    h1{margin:0;font-size:18px}
    .wrap{max-width:900px;margin:24px auto;padding:0 16px}
    .controls{display:flex;gap:8px}
    button{border:0;border-radius:999px;padding:10px 14px;cursor:pointer;background:#1d4ed8;color:#fff}
    button.secondary{background:#334155}
    .card{background:#1e293b;border:1px solid #334155;border-radius:16px;padding:16px;margin-top:12px}
    .meta{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#93c5fd;margin-bottom:8px}
    .cn{background:#0ea5e9;color:#00111a;padding:16px;border-radius:12px;text-align:center;font-size:20px;font-weight:600}
    .en{background:#0b1220;color:#93c5fd;padding:16px;border-radius:12px;text-align:center;font-size:16px;margin-top:8px}
    .hint{color:#93c5fd;text-align:center;margin-top:8px}
  </style>
</head>
<body>
  <header>
    <h1>Flashcards · Chinese → English</h1>
    <nav class="controls">
      <button id="shuffle">Shuffle</button>
      <button id="next" class="secondary">Next</button>
      <button id="reveal" class="secondary">Reveal</button>
    </nav>
  </header>

  <div class="wrap">
    <div id="card" class="card" tabindex="0" role="group" aria-label="flashcard">
      <div class="meta"><span id="category">—</span><span id="type">—</span></div>
      <div id="cn" class="cn">Loading…</div>
      <div id="hint" class="hint">Click “Reveal” to show English</div>
      <div id="en" class="en" style="display:none;"></div>
    </div>
  </div>

  <script>
    const state = { data: [], i: 0, revealed: false };
    const $ = id => document.getElementById(id);

    function render(){
      if(!state.data.length){
        $('cn').textContent='No data';
        $('hint').style.display='none';
        $('en').style.display='none';
        return;
      }
      const item = state.data[state.i % state.data.length];
      $('category').textContent = item.category || '—';
      $('type').textContent = item.type || '—';
      $('cn').textContent = item.chinese || '—'; // only this line shows Chinese
      $('en').textContent = item.english || '—';
      $('hint').style.display = state.revealed ? 'none' : 'block';
      $('en').style.display   = state.revealed ? 'block' : 'none';
    }

    function shuffle(a){
      for(let i=a.length-1;i>0;i--){
        const j=(Math.random()*(i+1))|0; [a[i],a[j]]=[a[j],a[i]];
      }
      return a;
    }

    $('reveal').onclick = ()=>{ state.revealed = !state.revealed; render(); };
    $('next').onclick   = ()=>{ state.i = (state.i+1)%state.data.length; state.revealed=false; render(); };
    $('shuffle').onclick= ()=>{ state.data = shuffle(state.data.slice()); state.i=0; state.revealed=false; render(); };

    window.addEventListener('keydown',e=>{
      if(e.code==='Space'){ e.preventDefault(); $('reveal').click(); }
      if(e.code==='ArrowRight'){ e.preventDefault(); $('next').click(); }
    });

    fetch('/flashcards').then(r=>r.json()).then(d=>{
      state.data = Array.isArray(d) ? d : (d.flashcards || []);
      render();
    }).catch(()=>{
      $('cn').textContent='Load failed';
      $('hint').style.display='none';
    });
  </script>
</body>
</html>
""", mimetype="text/html; charset=utf-8")

@app.route('/flashcards')
def get_flashcards():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "data.json is not valid JSON"}), 500

if __name__ == '__main__':
    app.run(debug=True)
