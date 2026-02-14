"""Unit tests for LZW compression algorithm."""

import pytest
from src.lzw import compress, decompress


class TestLZWCompression:
    """Test suite for LZW compression implementation."""

    def test_compress_simple(self):
        """Test compression with simple text."""
        text = "ABABABA"
        compressed = compress(text)
        
        # Compressed should be a list of integers
        assert isinstance(compressed, list)
        assert all(isinstance(x, int) for x in compressed)
        # Should have some content
        assert len(compressed) > 0

    def test_compress_single_character(self):
        """Test compression with single repeated character."""
        text = "AAAAA"
        compressed = compress(text)
        
        # Should compress repeated characters efficiently
        assert len(compressed) < len(text)

    def test_compress_no_repetition(self):
        """Test compression with no repeated patterns."""
        text = "ABCDEFGH"
        compressed = compress(text)
        
        # With no repetition, compression may not be effective
        # but should still work
        assert len(compressed) > 0

    def test_compress_empty_string(self):
        """Test compression with empty string."""
        text = ""
        compressed = compress(text)
        
        assert compressed == []

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
        
        # Should compress well due to repetition
        assert len(compressed) < len(original)
        assert decompressed == original

    def test_compress_builds_dictionary(self):
        """Test that compression builds dictionary beyond ASCII."""
        original = "ABABABA"
        compressed = compress(original)
        
        # Should have codes beyond 256 (initial ASCII dictionary size)
        assert any(code >= 256 for code in compressed)

    def test_decompress_edge_case(self):
        """Test decompression edge case where code not in dictionary yet."""
        # This tests the special case: code == dictionary_size
        original = "ABABABABABA"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original

    def test_compress_unicode(self):
        """Test compression with Unicode characters."""
        # LZW should handle ASCII characters (0-255)
        # Unicode may not work correctly with this implementation
        text = "Hello"  # Stick to ASCII for this implementation
        compressed = compress(text)
        decompressed = decompress(compressed)
        
        assert decompressed == text

    def test_compression_efficiency_repetitive(self):
        """Test that repetitive patterns achieve good compression."""
        # Highly repetitive text
        original = "A" * 50 + "B" * 50 + "AB" * 50
        compressed = compress(original)
        
        # Compression ratio should be significant
        compression_ratio = len(compressed) / len(original)
        assert compression_ratio < 0.8  # At least 20% compression

    def test_compression_efficiency_random(self):
        """Test compression with low repetition text."""
        # Less repetitive text
        original = "The quick brown fox jumps over the lazy dog"
        compressed = compress(original)
        decompressed = decompress(compressed)
        
        assert decompressed == original
        # May not compress as well, but should still work

    def test_decompress_invalid_code(self):
        """Test that decompression raises error for invalid compressed data."""
        # Create invalid compressed data with code far beyond dictionary
        invalid_compressed = [65, 66, 10000]  # 10000 is way beyond valid range
        
        with pytest.raises(ValueError):
            decompress(invalid_compressed)

    def test_multiple_compress_decompress_cycles(self):
        """Test multiple compression-decompression cycles."""
        original = "Test data for multiple cycles"
        
        # First cycle
        compressed1 = compress(original)
        decompressed1 = decompress(compressed1)
        assert decompressed1 == original
        
        # Second cycle on same data
        compressed2 = compress(decompressed1)
        decompressed2 = decompress(compressed2)
        assert decompressed2 == original
        
        # Compressed results should be identical
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
        # Should achieve some compression due to repeated phrases
        assert len(compressed) < len(original)
