def chunk_text(text, chunk_size=100, overlap=10):
    """
    Split text into chunks based on words with optional overlap.
    """
    if not text:
        return []

    words = text.split()
    chunks = []
    start = 0
    total_words = len(words)

    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap  # move forward with overlap

    return chunks
