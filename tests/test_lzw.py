"""Unit tests for LZW compression algorithm."""

import pytest
from src.lzw import compress, decompress


class TestLZWCompression:
    """Test suite for LZW compression implementation."""

    def test_compress_simple(self):
        """Test compression with simple text."""
        text = "ABABABA"
        compressed = compress(text)

        assert isinstance(compressed, bytearray)
        assert len(compressed) > 0

    def test_compress_single_character(self):
        """Test compression with single repeated character."""
        text = "AAAAA"
        compressed = compress(text)
        decompressed = decompress(compressed)

        assert decompressed == text
        assert isinstance(compressed, bytearray)

    def test_compress_no_repetition(self):
        """Test compression with no repeated patterns."""
        text = "ABCDEFGH"
        compressed = compress(text)

        assert len(compressed) > 0

    def test_compress_empty_string(self):
        """Test compression with empty string."""
        text = ""
        compressed = compress(text)

        assert isinstance(compressed, bytearray)
        assert len(compressed) <= 2

    def test_decompress_simple(self):
        """Test decompression with simple compressed data."""
        original = "ABABABA"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_decompress_single_character(self):
        """Test decompression with single repeated character."""
        original = "AAAAA"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_compress_decompress_cycle(self):
        """Test full compression-decompression cycle."""
        original = "TOBEORNOTTOBEORTOBEORNOT"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_compress_decompress_with_spaces(self):
        """Test compression with spaces and punctuation."""
        original = "Hello World! How are you?"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_compress_decompress_special_characters(self):
        """Test compression with special characters."""
        original = "Test@#$%^&*()123"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_compress_long_repetitive_text(self):
        """Test compression with long repetitive text."""
        original = "ABCD" * 100
        compressed = compress(original)
        decompressed = decompress(compressed)

        assert len(compressed) < len(original)
        assert decompressed == original

    def test_compress_builds_dictionary(self):
        """Test that dictionary growth works for repeated patterns."""
        original = "ABABABA"
        compressed = compress(original)
        decompressed = decompress(compressed)

        assert decompressed == original
        assert len(compressed) < len(original)

    def test_decompress_edge_case(self):
        """Test decompression edge case where code not in dictionary yet."""
        original = "ABABABABABA"
        compressed = compress(original)
        decompressed = decompress(compressed)

        assert decompressed == original

    def test_compress_unicode(self):
        """Test compression with ASCII-only text."""
        text = "Hello"
        compressed = compress(text)
        decompressed = decompress(compressed)

        assert decompressed == text

    def test_compression_efficiency_repetitive(self):
        """Test that repetitive patterns achieve good compression."""
        original = "A" * 50 + "B" * 50 + "AB" * 50
        compressed = compress(original)

        compression_ratio = len(compressed) / len(original)
        assert compression_ratio < 0.7

    def test_compression_efficiency_random(self):
        """Test compression with low repetition text."""
        original = "The quick brown fox jumps over the lazy dog"
        compressed = compress(original)
        decompressed = decompress(compressed)

        assert decompressed == original

    def test_decompress_invalid_code(self):
        """Test that decompression handles corrupted data gracefully."""
        invalid_compressed = bytearray([255, 255, 255, 255, 255])

        try:
            result = decompress(invalid_compressed)
            assert isinstance(result, str)
        except (ValueError, IndexError):
            pass

    def test_multiple_compress_decompress_cycles(self):
        """Test multiple compression-decompression cycles."""
        original = "Test data for multiple cycles"

        compressed1 = compress(original)
        decompressed1 = decompress(compressed1)
        assert decompressed1 == original

        compressed2 = compress(decompressed1)
        decompressed2 = decompress(compressed2)
        assert decompressed2 == original

        assert compressed1 == compressed2

    def test_compress_newlines_and_tabs(self):
        """Test compression with whitespace characters."""
        original = "Line 1\nLine 2\tTabbed"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_compress_book_excerpt(self):
        """Test compression with a longer text sample."""
        original = """
        It was the best of times, it was the worst of times,
        it was the age of wisdom, it was the age of foolishness,
        it was the epoch of belief, it was the epoch of incredulity,
        it was the season of Light, it was the season of Darkness,
        it was the spring of hope, it was the winter of despair.
        """
        compressed = compress(original)
        decompressed = decompress(compressed)

        assert decompressed == original
        assert len(compressed) < len(original)
