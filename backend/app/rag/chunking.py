import hashlib
import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    chunk_index: int
    checksum: str


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 900, chunk_overlap: int = 150) -> list[Chunk]:
    """Simple recursive-ish sliding window chunker on sentence boundaries."""
    text = clean_text(text)
    if not text:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks: list[Chunk] = []
    current = ""
    idx = 0

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= chunk_size:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(_make_chunk(current, idx))
                idx += 1
            # start new chunk, carry over overlap from tail of previous
            overlap_text = current[-chunk_overlap:] if current else ""
            current = f"{overlap_text} {sentence}".strip()

    if current:
        chunks.append(_make_chunk(current, idx))

    return chunks


def _make_chunk(text: str, idx: int) -> Chunk:
    checksum = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return Chunk(text=text, chunk_index=idx, checksum=checksum)


def document_checksum(text: str) -> str:
    return hashlib.sha256(clean_text(text).encode("utf-8")).hexdigest()
