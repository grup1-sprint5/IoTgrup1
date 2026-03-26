#!/usr/bin/env python3
"""
Mock de la Raspberry Pi Flask API per provar l'actuador.

Exposa:
  POST /actuator    -> accepta JSON {"state": "ON"|"OFF"} i respon amb l'estat
  GET  /status      -> retorna l'estat actual

No necessita depèndencies externes (només stdlib).
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

CURRENT_STATE = "OFF"


class Handler(BaseHTTPRequestHandler):
    def _set_json(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        global CURRENT_STATE
        if self.path != '/actuator':
            self._set_json(404)
            self.wfile.write(json.dumps({'success': False, 'message': 'Not Found'}).encode())
            return

        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8') if length else ''
        try:
            data = json.loads(body) if body else {}
        except Exception:
            self._set_json(400)
            self.wfile.write(json.dumps({'success': False, 'message': 'Invalid JSON'}).encode())
            return

        state = str(data.get('state', '')).upper()
        if state not in ('ON', 'OFF'):
            self._set_json(400)
            self.wfile.write(json.dumps({'success': False, 'message': 'Invalid state', 'current_state': CURRENT_STATE}).encode())
            return

        # Simula l'acció hardware
        CURRENT_STATE = state
        print(f"[raspi_mock] LED set to {CURRENT_STATE}")

        self._set_json(200)
        self.wfile.write(json.dumps({'success': True, 'message': 'State updated', 'current_state': CURRENT_STATE}).encode())

    def do_GET(self):
        if self.path != '/status':
            self._set_json(404)
            self.wfile.write(json.dumps({'success': False, 'message': 'Not Found'}).encode())
            return

        self._set_json(200)
        self.wfile.write(json.dumps({'success': True, 'current_state': CURRENT_STATE}).encode())


def run(port=5000):
    server = HTTPServer(('0.0.0.0', port), Handler)
    print(f"raspi_mock listening on http://0.0.0.0:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nraspi_mock stopping')
        server.server_close()


if __name__ == '__main__':
    run()
