import json
from http.server import BaseHTTPRequestHandler

from .auto_discovery import AutoDiscovery
from .problems import maxcut_triangle


HTML = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Virgin.IA Lab</title>
<style>
body{font-family:system-ui;margin:0;background:#0b1020;color:#eef2ff}main{max-width:1000px;margin:auto;padding:24px}
section{background:#141b31;border:1px solid #2b3555;border-radius:16px;padding:20px;margin:16px 0}
button{padding:12px 18px;border:0;border-radius:10px;cursor:pointer;font-weight:700}button:disabled{opacity:.5;cursor:wait}
textarea,input{width:100%;box-sizing:border-box;padding:10px;margin:8px 0;background:#0d1428;color:white;border:1px solid #394466;border-radius:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.metric{font-size:25px;font-weight:700}.muted{color:#aab4d0}.ok{color:#62d394}.error{color:#ff8d8d}
</style></head>
<body><main>
<h1>Virgin.IA <span class="muted">Laboratorio</span></h1>
<p class="muted">Descubrimiento automático de circuitos cuánticos.</p>
<section><h2>Prueba controlada</h2>
<label>Problema de referencia</label>
<textarea readonly>MaxCut de 3 nodos: encontrar un circuito que maximice el número de aristas cortadas.</textarea>
<label>Generaciones</label><input id="gen" type="number" min="1" max="20" value="3">
<button id="runBtn" onclick="run()">Ejecutar descubrimiento</button><p id="status" class="muted"></p></section>
<section><h2>Resultado</h2><div class="grid">
<div><span class="muted">Estado</span><div id="state" class="metric">—</div></div>
<div><span class="muted">Reward</span><div id="reward" class="metric">—</div></div>
<div><span class="muted">Mejor score</span><div id="score" class="metric">—</div></div>
<div><span class="muted">Probabilidad óptima</span><div id="prob" class="metric">—</div></div>
<div><span class="muted">Profundidad</span><div id="depth" class="metric">—</div></div>
</div></section>
<section><h2>Ciclo ejecutado</h2><ol><li>Define el problema.</li><li>Genera arquitecturas candidatas.</li><li>Simula cada circuito.</li><li>Evalúa calidad y coste.</li><li>Muta y selecciona candidatos.</li><li>Compara estrategias.</li><li>Guarda el experimento.</li></ol></section>
</main>
<script>
async function run(){
 const btn=document.getElementById('runBtn'), status=document.getElementById('status'); btn.disabled=true;
 document.getElementById('state').textContent='EJECUTANDO'; status.textContent='Buscando y evaluando circuitos...'; status.className='muted';
 try{const r=await fetch('/api/run',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({generations:Number(document.getElementById('gen').value)})});
 const d=await r.json(); if(!r.ok) throw new Error(d.error||'Error de ejecución');
 document.getElementById('state').textContent='COMPLETADO'; document.getElementById('state').className='metric ok';
 document.getElementById('reward').textContent=Number(d.reward).toFixed(4); document.getElementById('score').textContent=d.best_score;
 document.getElementById('prob').textContent=(100*Number(d.success_probability)).toFixed(1)+'%'; document.getElementById('depth').textContent=d.circuit_depth;
 status.textContent='Prueba completada correctamente.';
 }catch(e){document.getElementById('state').textContent='ERROR';document.getElementById('state').className='metric error';status.textContent=e.message;status.className='error';}
 finally{btn.disabled=false;}
}
</script></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def _send(self, body: bytes, status: int, content_type: str):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ('/', '/api', '/api/'):
            self._send(HTML.encode(), 200, 'text/html; charset=utf-8')
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path not in ('/api/run', '/run'):
            self.send_error(404); return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            payload = json.loads(self.rfile.read(size) or '{}')
            generations = max(1, min(20, int(payload.get('generations', 3))))
            result = AutoDiscovery().run(maxcut_triangle(), generations=generations)
            data = {
                'reward': result.experiment.reward,
                'best_score': result.experiment.best_score,
                'success_probability': result.experiment.success_probability,
                'circuit_depth': result.experiment.circuit_depth,
                'strategy': result.experiment.strategy,
            }
            self._send(json.dumps(data).encode(), 200, 'application/json')
        except Exception as exc:
            self._send(json.dumps({'error': str(exc)}).encode(), 500, 'application/json')


handler = Handler
