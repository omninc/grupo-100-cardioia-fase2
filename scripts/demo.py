"""Servidor de demonstração local. Não usar com dados reais ou em produção."""
import json
import sys
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.classificador import executar
from src.extracao import extrair, carregar_mapa

modelo, _, _, _, _ = executar()
mapa = carregar_mapa()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/analisar':
            frase = parse_qs(parsed.query).get('frase', [''])[0].strip()
            if not frase or len(frase) > 1000:
                self.send_error(400, 'Use uma frase ficticia de 1 a 1000 caracteres.')
                return
            r = extrair(frase, mapa)
            r['classe'] = modelo.predict([frase])[0]
            payload = json.dumps(r, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(payload)
        else:
            super().do_GET()

    def log_message(self, *_):
        pass  # Não registrar textos enviados à demonstração.


if __name__ == '__main__':
    print('Demonstração em http://127.0.0.1:8765/document/demo.html', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 8765), Handler).serve_forever()
