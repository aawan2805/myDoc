import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select

from app.db.models import Chunk, Document
from app.utils.logger import AppLogger

log = AppLogger("db")

load_dotenv()

DB_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
print(f"DB_URL: {DB_URL}")
engine = create_engine(DB_URL)

class DB:
    """Uso:
        with DB() as db:
            doc = db.add_to_documents("dni.pdf")
            db.add_to_chunks(doc.id, "texto", embedding)
    """

    def __enter__(self):
        # expire_on_commit=False: los objetos siguen usables después del with
        self.session = Session(engine, expire_on_commit=False)
        return self

    def __exit__(self, exc_type, exc, tb):
        # Si todo fue bien se guardan los cambios; si hubo error, se deshacen
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
            log.error(f"Cambios deshechos por un error: {exc}")
        self.session.close()

    def add_to_documents(self, filename: str) -> Document:
        document = Document(filename=filename)
        self.session.add(document)
        self.session.flush()
        log.info(f"Documento añadido: {filename} ({document.id})")
        return document

    def add_to_chunks(self, document: Document, content: str, embedding: list[float]) -> Chunk:
        chunk = Chunk(document=document, content=content, embedding=embedding)
        self.session.add(chunk)
        self.session.flush()
        return chunk

    def get_documents(self) -> list[Document]:
        return list(self.session.exec(select(Document)).all())

    def get_chunks(self, document: Document | None = None) -> list[Chunk]:
        """Todos los chunks, o solo los de un documento si se pasa."""
        query = select(Chunk)
        if document is not None:
            query = query.where(Chunk.document_id == document.id)
        return list(self.session.exec(query).all())
