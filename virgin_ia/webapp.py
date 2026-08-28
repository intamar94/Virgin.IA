from dataclasses import asdict
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from .auto_discovery import AutoDiscovery
from .problems import maxcut_triangle


HTML = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Virgin.IA Lab</title><style>body{font-family:system-ui;margin:0;background:#0b1020;color:#eef2ff}main{max-width:1000px;margin:auto;padding:32px}section{background:#141b31;border:1px solid #2b3555;border-radius:16px;padding:20px;margin:16px 0}button{padding:12px 18px;border:0;border-radius:10px;cursor:pointer}textarea,input{width:100%;box-sizing:border-box;padding:10px;margin:8px 0;background:#0d1428;color:white;border:1px solid #394466;border-radius:8px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.metric{font-size:26px;font-weight:700}.muted{color:#aab4d0}.ok{color:#62d394}</style></head><body><main><h1>Virgin.IA <span class="muted">Laboratorio</span></h1><p class="muted">Diseña, ejecuta y compara experimentos de descubrimiento cuántico.</p><section><h2>Nuevo experimento</h2><label>Problema</label><textarea id="problem">Selección de proyectos: maximizar beneficio con presupuesto y restricciones.</textarea><div class="grid"><div><label>Generaciones</label><input id="gen" type="number" min="1" max="20" value="2"></div><div><label>Población</label><input type="text" value="8" disabled></div></div><button onclick="run()">Ejecutar descubrimiento</button><p id="status" class="muted"></p></section><section><h2>Resultado</h2><div class="grid"><div><span class="muted">Estado</span><div id="state" class="metric">—</div></div><div><span class="muted">Reward</span><div id="reward" class="metric">—</div></div><div><span class="muted">Mejor score</span><div id="score" class="metric">—</div></div><div><span class="muted">Probabilidad</span><div id="prob" class="metric">—</div></div></div></section><section><h2>Qué hizo Virgin.IA</h2><ol><li>Formuló el problema.</li><li>Generó candidatos.</li><li>Simuló los circuitos.</li><li>Evaluó recompensa.</li><li>Mutó y seleccionó candidatos.</li><li>Guardó el experimento.</li></ol></section><section><h2>Experimentos</h2><p class="muted">Los resultados se conservan para futuras comparaciones y aprendizaje.</p></section></main><script>async function run(){let s=document.getElementById('status');s.textContent='Ejecutando búsqueda...';try{let r=await fetch('/api/run',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({generations:+document.getElementById('gen').value,problem:document.getElementById('problem').value})});let d=await r.json();if(!r.ok)throw Error(d.error||'Error');document.getElementById('state').textContent='COMPLETADO';document.getElementById('state').className='metric ok';document.getElementById('reward').textContent=d.reward.toFixed(4);document.getElementById('score').textContent=d.best_score;document.getElementById('prob').textContent=(100*d.success_probability).toFixed(1)+'%';s.textContent='Experimento terminado correctamente.'}catch(e){document.getElementById('state').textContent='ERROR';s.textContent=e.message}}</script></body></html>'''


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(404); return
        body = HTML.encode()
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)

    def do_POST(self):
        if self.path != '/api/run': self.send_error(404); return
        try:
            size=int(self.headers.get('Content-Length','0')); payload=json.loads(self.rfile.read(size) or '{}')
            result=AutoDiscovery().run(maxcut_triangle(), generations=max(1,min(20,int(payload.get('generations',2)))))
            data={'reward':result.experiment.reward,'best_score':result.experiment.best_score,'success_probability':result.experiment.success_probability}
            body=json.dumps(data).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
        except Exception as exc:
            body=json.dumps({'error':str(exc)}).encode(); self.send_response(500); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)


def serve(host='0.0.0.0', port=8000):
    HTTPServer((host,port),Handler).serve_forever()

if __name__ == '__main__': serve()
