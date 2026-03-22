"""Performance comparison tests for Huffman and LZW using natural language text."""

import sys
from pathlib import Path
from time import perf_counter

import pytest


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.huffman import HuffmanCoding
from src.lzw import compress as lzw_compress
from src.lzw import decompress as lzw_decompress


TEST_SIZES = [
    ("1 kB", 1_000),
    ("4 kB", 4_000),
    ("16 kB", 16_000),
    ("64 kB", 64_000),
    ("256 kB", 256_000),
    ("1 MB", 1_000_000),
    ("4 MB", 4_000_000),
    ("16 MB", 16_000_000),
]

SOURCE_GLOB = "wiki_*"


def _read_source_bytes() -> bytes:
    source_files = sorted(PROJECT_ROOT.glob(SOURCE_GLOB))
    if not source_files:
        pytest.skip(f"No source files found with pattern: {SOURCE_GLOB}")

    corpus = bytearray()
    for source_file in source_files:
        corpus.extend(source_file.read_bytes())

    if not corpus:
        pytest.skip("Source corpus is empty")

    return bytes(corpus)


def _decode_prefix_of_size(data: bytes, size_in_bytes: int) -> tuple[str, int]:
    """Return a Latin-1 text prefix of exactly size_in_bytes, expanding corpus if needed."""
    if len(data) >= size_in_bytes:
        chunk = data[:size_in_bytes]
    else:
        repeats = (size_in_bytes + len(data) - 1) // len(data)
        expanded = data * repeats
        chunk = expanded[:size_in_bytes]

    return chunk.decode("latin-1"), len(chunk)


def _huffman_compress_and_decompress(text: str) -> tuple[bytearray, str]:
    coder = HuffmanCoding("unused.txt")

    frequency = coder.make_frequency_dict(text)
    coder.make_heap(frequency)
    coder.merge_nodes()
    coder.make_codes()

    encoded_text = coder.get_encoded_text(text)
    padded = coder.pad_encoded_text(encoded_text)
    compressed = coder.get_byte_array(padded)

    bit_string = "".join(f"{byte:08b}" for byte in compressed)
    unpadded = coder.remove_padding(bit_string)
    decoded = coder.decode_text(unpadded)

    return compressed, decoded


@pytest.mark.slow
def test_natural_text_performance_by_size():
    """Compare compression ratio and runtime for both algorithms on natural text."""
    source_bytes = _read_source_bytes()

    rows = []
    for label, target_size in TEST_SIZES:
        text, actual_size = _decode_prefix_of_size(source_bytes, target_size)
        original_size = len(text.encode("latin-1"))

        huff_start = perf_counter()
        huff_compressed, huff_decompressed = _huffman_compress_and_decompress(text)
        huff_time = perf_counter() - huff_start

        lzw_start = perf_counter()
        lzw_compressed = lzw_compress(text)
        lzw_decompressed = lzw_decompress(lzw_compressed)
        lzw_time = perf_counter() - lzw_start

        assert huff_decompressed == text
        assert lzw_decompressed == text

        huff_ratio = len(huff_compressed) / original_size
        lzw_ratio = len(lzw_compressed) / original_size

        rows.append(
            {
                "size": label,
                "actual_size": actual_size,
                "huff_ratio": huff_ratio,
                "huff_time": huff_time,
                "lzw_ratio": lzw_ratio,
                "lzw_time": lzw_time,
            }
        )

    print("\nCompression benchmark (natural text from Plaintext Wikipedia (full English) Kaggle dataset)")
    print("size    | bytes   | huff_ratio | huff_time_s | lzw_ratio | lzw_time_s")
    for row in rows:
        print(
            f"{row['size']:7} | {row['actual_size']:7d} | "
            f"{row['huff_ratio']:.4f}     | {row['huff_time']:.6f}    | "
            f"{row['lzw_ratio']:.4f}    | {row['lzw_time']:.6f}"
        )


if __name__ == "__main__":
    test_natural_text_performance_by_size()
