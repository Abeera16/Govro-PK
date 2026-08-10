from app.rag.retriever import retrieve_gov_documents


async def rag_search(query: str, k: int = 5, category: str | None = None) -> list[dict]:
    return await retrieve_gov_documents(query=query, k=k, category=category)
