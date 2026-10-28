import uuid

import pytest
from sqlmodel import select

from app.db.db import DB
from app.db.models import EMBEDDING_DIM, Chunk, Document
from app.db.setup import setup_db
from app.embeddings.embeddings import embed_passages, embed_query


@pytest.fixture(scope="module", autouse=True)
def preparar_db():
    """Crea las tablas una vez antes de los tests."""
    setup_db()


@pytest.fixture
def db():
    """DB que deshace todo al terminar: los tests no dejan basura en la BD."""
    with DB() as db:
        yield db
        db.session.rollback()


def test_setup_db_se_puede_llamar_dos_veces():
    setup_db()


def test_add_to_documents_devuelve_document_con_uuid(db):
    doc = db.add_to_documents("test.pdf")
    assert isinstance(doc, Document)
    assert isinstance(doc.id, uuid.UUID)
    assert doc.filename == "test.pdf"


def test_add_to_chunks_guarda_el_chunk(db):
    doc = db.add_to_documents("test.pdf")
    vector = embed_passages(["hola"])[0]

    chunk = db.add_to_chunks(doc, "hola", vector)

    guardado = db.session.get(Chunk, chunk.id)
    assert guardado.document_id == doc.id
    assert guardado.content == "hola"
    assert len(guardado.embedding) == EMBEDDING_DIM
    assert doc.chunks == [guardado]


def test_get_documents_incluye_el_nuevo(db):
    doc = db.add_to_documents("test.pdf")
    ids = [d.id for d in db.get_documents()]
    assert doc.id in ids


def test_get_chunks_filtra_por_documento(db):
    doc_a = db.add_to_documents("a.pdf")
    doc_b = db.add_to_documents("b.pdf")
    vector = embed_passages(["x"])[0]
    db.add_to_chunks(doc_a, "de a", vector)
    db.add_to_chunks(doc_b, "de b", vector)

    chunks = db.get_chunks(doc_a)

    assert [c.content for c in chunks] == ["de a"]


def test_with_guarda_los_cambios_al_salir():
    with DB() as db:
        doc = db.add_to_documents("commit.pdf")

    # Nueva sesión: si se ve el documento es que se hizo commit
    with DB() as db:
        guardado = db.session.get(Document, doc.id)
        assert guardado is not None
        db.session.delete(guardado)


def test_with_deshace_los_cambios_si_hay_error():
    with pytest.raises(ValueError):
        with DB() as db:
            doc = db.add_to_documents("rollback.pdf")
            raise ValueError("fallo a propósito")

    with DB() as db:
        assert db.session.get(Document, doc.id) is None


def test_dimension_embedding_coincide_con_tabla():
    assert len(embed_query("hola")) == EMBEDDING_DIM


def test_busqueda_devuelve_el_chunk_mas_parecido(db):
    textos = [
        "Mi DNI caduca el 15/03/2030",
        "Mi número de la Seguridad Social es 08/1234567/89",
        "Estoy empadronado en la Calle Mayor 10",
    ]
    doc = db.add_to_documents("test.pdf")
    for texto, vector in zip(textos, embed_passages(textos)):
        db.add_to_chunks(doc, texto, vector)

    q = embed_query("¿Cuándo caduca mi DNI?")
    mejor = db.session.exec(
        select(Chunk)
        .where(Chunk.document_id == doc.id)
        .order_by(Chunk.embedding.cosine_distance(q))
        .limit(1)
    ).first()

    assert mejor.content == "Mi DNI caduca el 15/03/2030"
