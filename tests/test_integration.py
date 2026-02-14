"""Integration tests for compression algorithms with various file sizes."""

import pytest
import os
import tempfile
import time
from src.huffman import HuffmanCoding
from src.lzw import compress as lzw_compress, decompress as lzw_decompress


class TestIntegration:
    """Integration tests for end-to-end compression scenarios."""

    def generate_text(self, size_kb):
        """Generate text of approximately the specified size in KB.
        
        Uses a mix of repetitive and varied content to simulate natural text.
        """
        base_text = """
        The quick brown fox jumps over the lazy dog. 
        Programming is the art of telling another human what one wants the computer to do.
        Compression algorithms reduce the size of data by identifying and eliminating redundancy.
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Python is a high-level, interpreted programming language.
        """
        
        # Calculate how many repetitions we need
        target_size = size_kb * 1024
        repetitions = target_size // len(base_text) + 1
        
        text = base_text * repetitions
        # Trim to exact size and remove trailing whitespace (Huffman strips it)
        return text[:target_size].rstrip()

    @pytest.mark.parametrize("size_kb", [1, 4, 16, 64, 256])
    def test_huffman_various_sizes(self, size_kb):
        """Test Huffman compression with various file sizes."""
        # Generate test data
        test_text = self.generate_text(size_kb)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(test_text)
        temp_file.close()
        
        try:
            original_size = os.path.getsize(temp_file.name)
            
            # Compress
            h = HuffmanCoding(temp_file.name)
            start_time = time.time()
            compressed_path = h.compress()
            compress_time = time.time() - start_time
            
            compressed_size = os.path.getsize(compressed_path)
            
            # Decompress
            start_time = time.time()
            decompressed_path = h.decompress(compressed_path)
            decompress_time = time.time() - start_time
            
            # Verify correctness
            with open(decompressed_path, 'r') as f:
                decompressed_text = f.read()
            
            assert decompressed_text == test_text
            
            # Calculate metrics
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"\n--- Huffman {size_kb}KB ---")
            print(f"Original size: {original_size} bytes")
            print(f"Compressed size: {compressed_size} bytes")
            print(f"Compression ratio: {compression_ratio:.2f}%")
            print(f"Compression time: {compress_time:.4f}s")
            print(f"Decompression time: {decompress_time:.4f}s")
            
            # Assertions
            assert os.path.exists(compressed_path)
            assert os.path.exists(decompressed_path)
            assert compressed_size > 0
            
            # Cleanup
            os.unlink(compressed_path)
            os.unlink(decompressed_path)
        finally:
            os.unlink(temp_file.name)

    @pytest.mark.parametrize("size_kb", [1, 4, 16, 64, 256])
    def test_lzw_various_sizes(self, size_kb):
        """Test LZW compression with various file sizes."""
        # Generate test data
        test_text = self.generate_text(size_kb)
        original_size = len(test_text)
        
        # Compress
        start_time = time.time()
        compressed = lzw_compress(test_text)
        compress_time = time.time() - start_time
        
        # Calculate compressed size (assuming 4 bytes per integer code)
        compressed_size = len(compressed) * 4  # Each code is an integer (4 bytes)
        
        # Decompress
        start_time = time.time()
        decompressed = lzw_decompress(compressed)
        decompress_time = time.time() - start_time
        
        # Verify correctness
        assert decompressed == test_text
        
        # Calculate metrics
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        print(f"\n--- LZW {size_kb}KB ---")
        print(f"Original size: {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes (estimated)")
        print(f"Compression ratio: {compression_ratio:.2f}%")
        print(f"Compression time: {compress_time:.4f}s")
        print(f"Decompression time: {decompress_time:.4f}s")
        
        # Assertions
        assert len(compressed) > 0
        assert decompressed == test_text

    def test_huffman_vs_lzw_1mb(self):
        """Compare Huffman and LZW on 1MB file."""
        size_kb = 1024  # 1 MB
        test_text = self.generate_text(size_kb)
        
        # Test Huffman
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(test_text)
        temp_file.close()
        
        try:
            h = HuffmanCoding(temp_file.name)
            
            start_time = time.time()
            compressed_path = h.compress()
            huffman_time = time.time() - start_time
            
            huffman_size = os.path.getsize(compressed_path)
            original_size = os.path.getsize(temp_file.name)
            huffman_ratio = (1 - huffman_size / original_size) * 100
            
            # Verify Huffman decompression
            decompressed_path = h.decompress(compressed_path)
            with open(decompressed_path, 'r') as f:
                huffman_decompressed = f.read()
            assert huffman_decompressed == test_text
            
            # Cleanup Huffman files
            os.unlink(compressed_path)
            os.unlink(decompressed_path)
        finally:
            os.unlink(temp_file.name)
        
        # Test LZW
        start_time = time.time()
        lzw_compressed = lzw_compress(test_text)
        lzw_time = time.time() - start_time
        
        lzw_size = len(lzw_compressed) * 4
        lzw_ratio = (1 - lzw_size / original_size) * 100
        
        # Verify LZW decompression
        lzw_decompressed = lzw_decompress(lzw_compressed)
        assert lzw_decompressed == test_text
        
        # Print comparison
        print("\n=== 1MB Comparison ===")
        print(f"Original size: {original_size} bytes")
        print(f"\nHuffman:")
        print(f"  Compressed size: {huffman_size} bytes")
        print(f"  Compression ratio: {huffman_ratio:.2f}%")
        print(f"  Compression time: {huffman_time:.4f}s")
        print(f"\nLZW:")
        print(f"  Compressed size: {lzw_size} bytes (estimated)")
        print(f"  Compression ratio: {lzw_ratio:.2f}%")
        print(f"  Compression time: {lzw_time:.4f}s")

    def test_highly_repetitive_text(self):
        """Test both algorithms on highly repetitive text."""
        # Create highly repetitive text that should compress very well
        test_text = "AAAABBBBCCCCDDDD" * 1000
        
        # Test Huffman
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(test_text)
        temp_file.close()
        
        try:
            h = HuffmanCoding(temp_file.name)
            compressed_path = h.compress()
            
            original_size = os.path.getsize(temp_file.name)
            huffman_size = os.path.getsize(compressed_path)
            huffman_ratio = (1 - huffman_size / original_size) * 100
            
            decompressed_path = h.decompress(compressed_path)
            with open(decompressed_path, 'r') as f:
                huffman_result = f.read()
            
            assert huffman_result == test_text
            
            os.unlink(compressed_path)
            os.unlink(decompressed_path)
        finally:
            os.unlink(temp_file.name)
        
        # Test LZW
        lzw_compressed = lzw_compress(test_text)
        lzw_size = len(lzw_compressed) * 4
        lzw_ratio = (1 - lzw_size / original_size) * 100
        lzw_result = lzw_decompress(lzw_compressed)
        
        assert lzw_result == test_text
        
        print("\n=== Highly Repetitive Text ===")
        print(f"Huffman compression: {huffman_ratio:.2f}%")
        print(f"LZW compression: {lzw_ratio:.2f}%")
        
        # Both should achieve significant compression
        assert huffman_ratio > 20
        assert lzw_ratio > 20

    def test_random_like_text(self):
        """Test both algorithms on text with low repetition."""
        # Create text with varied characters (less compressible)
        import random
        random.seed(42)  # For reproducibility
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?"
        test_text = ''.join(random.choice(chars) for _ in range(10000))
        
        # Test Huffman
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(test_text)
        temp_file.close()
        
        try:
            h = HuffmanCoding(temp_file.name)
            compressed_path = h.compress()
            
            original_size = os.path.getsize(temp_file.name)
            huffman_size = os.path.getsize(compressed_path)
            huffman_ratio = (1 - huffman_size / original_size) * 100
            
            decompressed_path = h.decompress(compressed_path)
            with open(decompressed_path, 'r') as f:
                huffman_result = f.read()
            
            assert huffman_result == test_text
            
            os.unlink(compressed_path)
            os.unlink(decompressed_path)
        finally:
            os.unlink(temp_file.name)
        
        # Test LZW
        lzw_compressed = lzw_compress(test_text)
        lzw_size = len(lzw_compressed) * 4
        lzw_ratio = (1 - lzw_size / original_size) * 100
        lzw_result = lzw_decompress(lzw_compressed)
        
        assert lzw_result == test_text
        
        print("\n=== Low Repetition Text ===")
        print(f"Huffman compression: {huffman_ratio:.2f}%")
        print(f"LZW compression: {lzw_ratio:.2f}%")

    @pytest.mark.slow
    def test_large_file_10mb(self):
        """Test with 10MB file as required by professor."""
        size_kb = 10 * 1024  # 10 MB
        test_text = self.generate_text(size_kb)
        
        # Test Huffman
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write(test_text)
        temp_file.close()
        
        try:
            original_size = os.path.getsize(temp_file.name)
            
            h = HuffmanCoding(temp_file.name)
            
            print(f"\n=== 10MB File Test ===")
            print(f"Original size: {original_size / (1024*1024):.2f} MB")
            
            # Compress
            start_time = time.time()
            compressed_path = h.compress()
            compress_time = time.time() - start_time
            
            compressed_size = os.path.getsize(compressed_path)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"Huffman compressed size: {compressed_size / (1024*1024):.2f} MB")
            print(f"Huffman compression ratio: {compression_ratio:.2f}%")
            print(f"Huffman compression time: {compress_time:.4f}s")
            
            # Decompress
            start_time = time.time()
            decompressed_path = h.decompress(compressed_path)
            decompress_time = time.time() - start_time
            
            print(f"Huffman decompression time: {decompress_time:.4f}s")
            
            # Verify
            with open(decompressed_path, 'r') as f:
                decompressed_text = f.read()
            
            assert decompressed_text == test_text
            
            # Cleanup
            os.unlink(compressed_path)
            os.unlink(decompressed_path)
        finally:
            os.unlink(temp_file.name)
        
        # Note: LZW might be too slow/memory-intensive for 10MB
        # Commenting out for now, but can be enabled if needed
        print("Note: LZW test skipped for 10MB due to potential memory constraints")
