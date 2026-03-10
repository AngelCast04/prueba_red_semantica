#!/bin/bash
# Doble clic: levanta el servidor GraphRAG en http://localhost:8080

# Ir a la carpeta del proyecto (donde está este script)
cd "$(dirname "$0")"

# Activar venv y arrancar servidor
echo "Iniciando servidor GraphRAG..."
echo "Abre en el navegador: http://localhost:8080"
echo "Para detener: Ctrl+C o cierra esta ventana."
echo ""

./venv/bin/python run_consulta.py

# Si el servidor se detiene, esperar antes de cerrar para ver mensajes de error
echo ""
read -p "Pulsa Enter para cerrar esta ventana..."
