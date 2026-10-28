from datetime import datetime, timezone
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlmodel import Column, Field, Relationship, SQLModel

# 384 = dimensiones del modelo intfloat/multilingual-e5-small
EMBEDDING_DIM = 384

class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    filename: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Como el related_name de Django: doc.chunks (solo dentro del with, con la sesión abierta)
    chunks: list["Chunk"] = Relationship(back_populates="document", cascade_delete=True)


class Chunk(SQLModel, table=True):
    __tablename__ = "chunks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    document_id: UUID = Field(foreign_key="documents.id", ondelete="CASCADE")
    content: str
    embedding: list[float] = Field(sa_column=Column(Vector(EMBEDDING_DIM)))

    document: Document = Relationship(back_populates="chunks")
