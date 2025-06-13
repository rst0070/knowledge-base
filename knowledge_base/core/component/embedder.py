from knowledge_base.core.port.embedder import Embedder
from fastembed import TextEmbedding


class FastEmbed(Embedder):
    def __init__(self, embedding_model: TextEmbedding):
        self.embedding_model = embedding_model

    def embed(self, text: str) -> list[float]:
        embedding_generator = self.embedding_model.embed(text)
        embedding = list(embedding_generator)
        embedding = embedding[0].tolist()
        return embedding
