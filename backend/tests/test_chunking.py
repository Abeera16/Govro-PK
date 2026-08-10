from app.rag.chunking import chunk_text, document_checksum


def test_chunk_text_basic():
    text = "This is sentence one. This is sentence two. This is sentence three." * 20
    chunks = chunk_text(text, chunk_size=100, chunk_overlap=20)
    assert len(chunks) > 1
    for c in chunks:
        assert len(c.text) > 0


def test_document_checksum_stable():
    text = "Hello world"
    assert document_checksum(text) == document_checksum("Hello   world")


def test_empty_text_returns_no_chunks():
    assert chunk_text("") == []
