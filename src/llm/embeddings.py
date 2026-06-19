from langchain_openai import OpenAIEmbeddings

from src.config.settings import settings

_embeddings = OpenAIEmbeddings(
    api_key=settings.openai_api_key,
    model=settings.openai_embedding_model,
)


def embed(text: str) -> list[float]:
    return _embeddings.embed_query(text)
