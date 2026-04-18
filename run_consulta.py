"""Lanza la interfaz web de consultas con GraphRAG."""

import os
import sys
from pathlib import Path

# Asegurar que estamos en el directorio del proyecto
base_dir = Path(__file__).resolve().parent
os.chdir(base_dir)

def _load_dotenv_fallback(dotenv_path: Path) -> None:
    """
    Carga un .env mínimo sin dependencias.
    - Soporta líneas KEY=VALUE
    - Ignora vacíos y comentarios (# ...)
    - No sobreescribe variables ya definidas en el entorno
    """
    if not dotenv_path.exists():
        return
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


# Cargar variables desde .env si existe (ruta explícita)
try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv(base_dir / ".env")
except ImportError:
    _load_dotenv_fallback(base_dir / ".env")

if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Configura OPENAI_API_KEY antes de ejecutar:")
    print("   PowerShell: $env:OPENAI_API_KEY='sk-tu-clave'")
    print("   CMD: set OPENAI_API_KEY=sk-tu-clave")
    print("   O usa el archivo .env en la raíz del proyecto.")
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
