# docs-rag — contexto del proyecto

## Qué es
Proyecto personal: una app RAG para consultar mis documentos personales (DNI, Seguridad Social, empadronamiento, certificados...). Subo PDFs y luego le pregunto al chat.

## Fases
1. **RAG básico (ahora):** embeddings, Postgres, búsqueda y respuesta del LLM.
2. **Agentes:** el RAG como herramienta de un agente; orquestación con LangGraph.
3. **Nube:** Docker, Kubernetes (primero Minikube en local, luego un clúster gestionado), CI/CD, gestión de secretos.

## Stack y decisiones
- **uv** para el proyecto y las dependencias. Python 3.12+.
- **FastAPI**, todo síncrono, **sin Celery** por ahora.
- **PostgreSQL + pgvector** instalado en Windows, **sin Docker** por ahora (pgvector compilado con nmake).
- **ORM: SQLModel** (con `pgvector.sqlalchemy.Vector`). Nada de SQL a mano salvo `CREATE EXTENSION vector`. URL: `postgresql+psycopg://...`
- **IDs UUID** en todas las tablas.
- **Embeddings en local** con `sentence-transformers` y el modelo `intfloat/multilingual-e5-small` (384 dimensiones). Prefijos obligatorios: `passage: ` para los trozos y `query: ` para las preguntas. Nada de APIs externas para embeddings: son datos sensibles.
- **Sin LangChain** por ahora; cada pieza a mano para entenderla.
- **Sin OCR** al principio; solo PDFs con texto (pymupdf).
- **LLM:** Seria LLM local, bien sea por OLLAMA o HUGGING FACE.
- **Logs:** clase propia `AppLogger` en `app/utils/logger.py`, métodos `ok` (verde), `info` (azul), `warning` (naranja), `error` (rojo). Simple, con `print` y colorama. Sin el módulo `logging`.
- **Tests con pytest** en `tests/`, nunca scripts sueltos tipo `prueba.py`. Los tests de BD hacen rollback y no dejan datos.

## Estructura actual
```
docs-rag/
├── app/
│   ├── db/
│   │   ├── models.py      # Document, Chunk (SQLModel, table=True)
│   │   ├── db.py          # clase DB (context manager: commit/rollback)
│   │   └── setup.py       # crea extensión y tablas: uv run python -m app.db.setup
│   ├── embeddings/
│   │   └── embeddings.py  # embed_passages, embed_query
│   └── utils/
│       └── logger.py      # AppLogger
├── tests/
│   ├── test_db.py
│   └── test_logs.py
└── pyproject.toml
```
- Es posible que actualmente esta estructura no se esté respetando, por lo que modificala para que quede como la que te he dado más arriba.
Clase `DB`:
```python
with DB() as db:
    doc = db.add_to_documents("dni.pdf")
    db.add_to_chunks(doc, "texto", embedding)
    db.get_documents()
    db.get_chunks(doc)  # o sin argumento: todos
```

## Siguientes pasos
1. `schemas.py` con modelos Pydantic de entrada/salida (equivalente a los serializers de DRF). No devolver el `embedding` en la API.
2. Ingesta: leer PDF, trocear, generar embeddings y guardar (+ tests).
3. Endpoints `/upload` y `/ask`.
4. Conectar el LLM.
5. Alembic para migraciones (en lugar de `create_all`).
6. Autenticación antes de desplegar.

## Cómo quiero trabajar
- En español, respuestas cortas y directas.
- Paso a paso: no avanzar al siguiente paso hasta que yo haya probado el anterior.
- Primero me vas a decir que harás, porque, y que archivos tocarás
- Código simple, sin sobreingeniería ni detalles que no he pedido.
- Organizado en carpetas por módulo.
- Vengo de Django (2 años de backend Python): las comparaciones con Django me ayudan.
- Trabajo en Windows con CMD y PowerShell.
- Una vez tengas mi permiso vas a hacer los cambios
- A medida de lo posible, quiero clases para todo, trabajar a modo POO
- A medida de lo posible, quiero también utilizar pydantic
- Por cada endpoint de la API que vayas a crear, tiene que estar muy bien documentada y tambien indicar y devolver los codigos (200, 400, 500, etc...)
- Para cualquier tipo de libreria que utilices me lo indicarás claramente el nombre de la libreria y la version a instalar y su compatibilidad con Windows
