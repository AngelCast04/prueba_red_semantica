"""Quickstart de fast-graphrag con PDFs de la carpeta libros."""

import os
from pathlib import Path

# Raíz del repo (build en Render puede tener cwd distinto al runtime de uvicorn)
_ROOT = Path(__file__).resolve().parent


def _resolve_dir(env_key: str, default_relative: str) -> str:
    raw = (os.getenv(env_key) or default_relative).strip() or default_relative
    p = Path(raw)
    if p.is_absolute():
        return str(p)
    return str((_ROOT / p).resolve())


# Cargar .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

import fitz  # PyMuPDF
from fast_graphrag import GraphRAG
from fast_graphrag._llm import OpenAIEmbeddingService, OpenAILLMService


def extraer_texto_pdf(ruta_pdf: str) -> str:
    """Extrae el texto de un archivo PDF."""
    doc = fitz.open(ruta_pdf)
    texto = ""
    for pagina in doc:
        texto += pagina.get_text()
    doc.close()
    return texto


def cargar_pdfs_carpeta(carpeta: str) -> str:
    """Carga y concatena el texto de todos los PDFs en una carpeta."""
    path = Path(carpeta)
    textos = []
    for archivo in sorted(path.glob("*.pdf")):
        if archivo.name.startswith("._"):
            continue
        print(f"Procesando: {archivo.name}")
        textos.append(extraer_texto_pdf(str(archivo)))
    return "\n\n---\n\n".join(textos)


DOMAIN = (
    "Analiza instrumentos internacionales y documentos de derechos humanos como un sistema integrado. "
    "Identifica estructuras jerárquicas: categorías generales (poblaciones, derechos) y sus desgloses "
    "a instrumentos, organismos, mecanismos y casos concretos. Facilita drill-down de lo general a lo específico."
)

EXAMPLE_QUERIES = [
    "¿Qué poblaciones vulnerables y derechos se cubren en los documentos?",
    "¿Qué instrumentos protegen a personas indígenas?",
    "¿Cuáles son los mecanismos de la ONU para migrantes y refugiados?",
    "¿Cómo se relacionan los tratados con resoluciones específicas por tema?",
    "¿Qué obligaciones de los Estados se mencionan para adultos mayores?",
]

ENTITY_TYPES = [
    "Población",
    "Derecho",
    "Tratado",
    "Resolución",
    "Organismo",
    "Mecanismo",
    "Concepto_Jurídico",
    "País",
    "Órgano",
]

# Límites de tasa para evitar error 429 (Rate limit exceeded)
# Ajusta según tu plan en platform.openai.com/account/rate-limits
_WORKDIR = _resolve_dir("GRAPH_WORKING_DIR", "grafo_libros")
_LIBROS = _resolve_dir("LIBROS_DIR", "libros")

grag = GraphRAG(
    working_dir=_WORKDIR,
    domain=DOMAIN,
    example_queries="\n".join(EXAMPLE_QUERIES),
    entity_types=ENTITY_TYPES,
    config=GraphRAG.Config(
        llm_service=OpenAILLMService(
            model="gpt-4o-mini",
            max_requests_concurrent=int(os.getenv("CONCURRENT_TASK_LIMIT", "4")),
            rate_limit_per_minute=True,
            max_requests_per_minute=30,
            rate_limit_concurrency=True,
        ),
        embedding_service=OpenAIEmbeddingService(
            max_requests_concurrent=4,
            rate_limit_per_minute=True,
            max_requests_per_minute=60,
            rate_limit_concurrency=True,
        ),
    ),
)

def bucle_consultas():
    """Bucle interactivo para drill-down: de lo general a lo específico."""
    print("\n" + "=" * 60)
    print("Modo drill-down: explora de lo general a lo específico.")
    print("Ejemplos: pregunta general → luego consultas más concretas.")
    print("Escribe 'salir' para terminar.")
    print("=" * 60)

    while True:
        try:
            consulta = input("\nTu consulta: ").strip()
            if not consulta:
                continue
            if consulta.lower() in ("salir", "exit", "quit"):
                print("Hasta luego.")
                break

            print("\nAnalizando...")
            respuesta = grag.query(consulta)
            print("\n--- Respuesta ---\n")
            print(respuesta.response)
            print("\n" + "-" * 40)

        except KeyboardInterrupt:
            print("\nHasta luego.")
            break
        except Exception as e:
            print(f"\nError: {e}")


texto = cargar_pdfs_carpeta(_LIBROS)
grag.insert(texto)

print("\n¡Grafos cargados! Iniciando modo consulta...")
bucle_consultas()
