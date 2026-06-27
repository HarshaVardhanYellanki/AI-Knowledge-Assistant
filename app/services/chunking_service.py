from typing import List


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def chunk_text(text: str) -> List[str]:

    words = text.split()

    chunks = []

    current_chunk = []

    current_length = 0

    for word in words:

        if current_length + len(word) + 1 <= CHUNK_SIZE:

            current_chunk.append(word)
            current_length += len(word) + 1

        else:

            chunks.append(
                " ".join(current_chunk)
            )

            overlap_words = []

            overlap_length = 0

            for overlap_word in reversed(current_chunk):

                overlap_length += len(overlap_word) + 1

                overlap_words.insert(
                    0,
                    overlap_word
                )

                if overlap_length >= CHUNK_OVERLAP:
                    break

            current_chunk = overlap_words

            current_chunk.append(word)

            current_length = len(
                " ".join(current_chunk)
            )

    if current_chunk:

        chunks.append(
            " ".join(current_chunk)
        )

    return chunks