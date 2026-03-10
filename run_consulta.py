"""Lanza la interfaz web de consultas con GraphRAG."""

import os
import sys
from pathlib import Path

# Asegurar que estamos en el directorio del proyecto
base_dir = Path(__file__).resolve().parent
os.chdir(base_dir)

# Cargar variables desde .env si existe (ruta explícita)
try:
    from dotenv import load_dotenv
    load_dotenv(base_dir / ".env")
except ImportError:
    pass

if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Configura OPENAI_API_KEY antes de ejecutar:")
    print("   export OPENAI_API_KEY='sk-tu-clave'")
    sys.exit(1)

try:
    import uvicorn
except ImportError:
    print("Instalando uvicorn y fastapi...")
    os.system(f"{sys.executable} -m pip install -q uvicorn fastapi")
    import uvicorn

if __name__ == "__main__":
    print("Iniciando interfaz de consultas en http://localhost:8080")
    print("Pulsa Ctrl+C para detener.\n")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
    )
