from fastembed import TextEmbedding


def get_fastembed_embedding_model(
    embedding_model: str,
) -> TextEmbedding:
    return TextEmbedding(model_name=embedding_model)
