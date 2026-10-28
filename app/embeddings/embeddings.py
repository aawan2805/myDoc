from sentence_transformers import SentenceTransformer

from app.utils.logger import AppLogger

log = AppLogger("embeddings")

MODEL_NAME = "intfloat/multilingual-e5-small"


class Embedder:
    """Genera embeddings en local. El modelo e5 exige prefijos:
    'passage: ' para los trozos de documento y 'query: ' para las preguntas.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        log.info(f"Cargando modelo {model_name}...")
        self.model = SentenceTransformer(model_name)
        log.ok("Modelo cargado")

    def embed_passages(self, texts: list[str]) -> list[list[float]]:
        vectors = self.model.encode([f"passage: {t}" for t in texts], normalize_embeddings=True)
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        vector = self.model.encode(f"query: {text}", normalize_embeddings=True)
        return vector.tolist()


# El modelo tarda en cargar: se crea una sola vez, la primera vez que se usa
_embedder: Embedder | None = None


def _get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder


def embed_passages(texts: list[str]) -> list[list[float]]:
    return _get_embedder().embed_passages(texts)


def embed_query(text: str) -> list[float]:
    return _get_embedder().embed_query(text)
