from pathlib import Path

def gen_paths(path):
    folderPath = Path(path)
    paths = []
    if folderPath.is_dir():
        for item in folderPath.iterdir():
            if item.is_file():
                paths.append(str(item))

    return paths

def chunk_caption_text(text: str, max_len: int = 40) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks = []
    current_chunk = ""
    for word in words:
        # Check if adding the next word exceeds max_len
        if not current_chunk:
            # Always add the first word
            current_chunk = word
        elif len(current_chunk) + len(word) + 1 <= max_len:
            # Add word to current chunk
            current_chunk += " " + word
        else:
            # Current chunk is full, start a new one
            chunks.append(current_chunk)
            current_chunk = word

    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
