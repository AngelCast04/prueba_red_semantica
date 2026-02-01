"""Exporta el grafo y lanza el servidor web para visualizarlo."""

import http.server
import os
import socketserver

# Ejecutar exportación
from export_grafo import main as export_main

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base)

    print("Exportando grafo...")
    export_main()

    vis_dir = os.path.join(base, "visualizer")
    os.chdir(vis_dir)
    port = 8080
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"\nAbre en el navegador: http://localhost:{port}")
        print("Pulsa Ctrl+C para detener el servidor.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
