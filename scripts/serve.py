#!/usr/bin/env python3
"""Tiny static server for the F-150 3D explorer (stdlib only).

Serves the repo root so /viewer/, /inventory/, and /manuals/ are all reachable.
Binds 127.0.0.1 only; expose to the tailnet with:
    tailscale serve --bg --https=443 http://127.0.0.1:8080
"""
import http.server, socketserver, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
HOST = os.environ.get("HOST", "127.0.0.1")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header("Location", "/viewer/")
            self.end_headers()
            return
        return super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass


with socketserver.ThreadingTCPServer((HOST, PORT), Handler) as httpd:
    httpd.allow_reuse_address = True
    print(f"F-150 explorer → http://{HOST}:{PORT}/  (serving {ROOT})")
    httpd.serve_forever()
