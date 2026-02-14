"""Unit tests for Huffman coding algorithm."""

import pytest
import os
import tempfile
from src.huffman import HuffmanCoding


class TestHuffmanCoding:
    """Test suite for Huffman coding implementation."""

    def test_frequency_dict_simple(self):
        """Test frequency calculation with simple text."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = h.make_frequency_dict("AAABBC")
        
        assert frequency == {'A': 3, 'B': 2, 'C': 1}
        os.unlink(temp_file.name)

    def test_frequency_dict_single_char(self):
        """Test frequency calculation with repeated single character."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = h.make_frequency_dict("AAAAA")
        
        assert frequency == {'A': 5}
        os.unlink(temp_file.name)

    def test_frequency_dict_empty(self):
        """Test frequency calculation with empty string."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = h.make_frequency_dict("")
        
        assert frequency == {}
        os.unlink(temp_file.name)

    def test_make_heap(self):
        """Test heap creation from frequency dictionary."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = {'A': 3, 'B': 2, 'C': 1}
        h.make_heap(frequency)
        
        # Check that heap has correct number of nodes
        assert len(h.heap) == 3
        # Check that heap property is maintained (min element first)
        assert h.heap[0].freq == 1  # C has frequency 1
        os.unlink(temp_file.name)

    def test_merge_nodes(self):
        """Test Huffman tree construction."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = {'A': 3, 'B': 2, 'C': 1}
        h.make_heap(frequency)
        h.merge_nodes()
        
        # After merging, heap should have only root node
        assert len(h.heap) == 1
        # Root frequency should be sum of all frequencies
        assert h.heap[0].freq == 6  # 3 + 2 + 1
        os.unlink(temp_file.name)

    def test_make_codes(self):
        """Test code generation from Huffman tree."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = {'A': 3, 'B': 2, 'C': 1}
        h.make_heap(frequency)
        h.merge_nodes()
        h.make_codes()
        
        # Check that codes were generated for all characters
        assert len(h.codes) == 3
        assert 'A' in h.codes
        assert 'B' in h.codes
        assert 'C' in h.codes
        
        # More frequent characters should have shorter or equal codes
        assert len(h.codes['A']) <= len(h.codes['C'])
        
        # Check reverse mapping exists
        assert len(h.reverse_mapping) == 3
        os.unlink(temp_file.name)

    def test_get_encoded_text(self):
        """Test text encoding using Huffman codes."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        frequency = {'A': 3, 'B': 2}
        h.make_heap(frequency)
        h.merge_nodes()
        h.make_codes()
        
        encoded = h.get_encoded_text("AABBA")
        
        # Check that encoding produces binary string
        assert all(c in '01' for c in encoded)
        # Length should be based on code lengths
        assert len(encoded) > 0
        os.unlink(temp_file.name)

    def test_pad_encoded_text(self):
        """Test padding of encoded text to byte boundary."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        
        # Test with text that needs padding
        encoded = "001"  # 3 bits
        padded = h.pad_encoded_text(encoded)
        
        # Should be divisible by 8
        assert len(padded) % 8 == 0
        # First 8 bits should contain padding info
        padding_info = int(padded[:8], 2)
        assert padding_info == 5  # 8 - 3 = 5 bits of padding needed
        os.unlink(temp_file.name)

    def test_get_byte_array(self):
        """Test conversion of binary string to byte array."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        
        # Test with valid padded text (16 bits = 2 bytes)
        padded_text = "0100101001100001"
        byte_array = h.get_byte_array(padded_text)
        
        assert len(byte_array) == 2
        assert byte_array[0] == int("01001010", 2)  # 74
        assert byte_array[1] == int("01100001", 2)  # 97
        os.unlink(temp_file.name)

    def test_get_byte_array_invalid_length(self):
        """Test that byte array conversion fails with invalid length."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        
        # Test with text not divisible by 8
        invalid_text = "0100101"  # 7 bits
        with pytest.raises(ValueError):
            h.get_byte_array(invalid_text)
        os.unlink(temp_file.name)

    def test_heap_node_comparison(self):
        """Test HeapNode comparison operators."""
        node1 = HuffmanCoding.HeapNode('A', 5)
        node2 = HuffmanCoding.HeapNode('B', 3)
        node3 = HuffmanCoding.HeapNode('C', 5)
        
        # Test less than
        assert node2 < node1
        assert not (node1 < node2)
        
        # Test equality
        assert node1 == node3
        assert not (node1 == node2)

    def test_compress_decompress_simple(self):
        """Test end-to-end compression and decompression with simple text."""
        # Create temporary input file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        test_text = "AAABBBCCCDDD"
        temp_file.write(test_text)
        temp_file.close()
        
        # Compress
        h = HuffmanCoding(temp_file.name)
        compressed_path = h.compress()
        
        # Check that compressed file exists and has content
        assert os.path.exists(compressed_path)
        compressed_size = os.path.getsize(compressed_path)
        assert compressed_size > 0
        
        # Decompress
        decompressed_path = h.decompress(compressed_path)
        
        # Read decompressed file and compare
        with open(decompressed_path, 'r') as f:
            decompressed_text = f.read()
        
        assert decompressed_text == test_text
        
        # Cleanup
        os.unlink(temp_file.name)
        os.unlink(compressed_path)
        os.unlink(decompressed_path)

    def test_compress_with_special_characters(self):
        """Test compression with special characters."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        test_text = "Hello, World! 123 @#$%"
        temp_file.write(test_text)
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)
        compressed_path = h.compress()
        decompressed_path = h.decompress(compressed_path)
        
        with open(decompressed_path, 'r') as f:
            decompressed_text = f.read()
        
        assert decompressed_text == test_text
        
        # Cleanup
        os.unlink(temp_file.name)
        os.unlink(compressed_path)
        os.unlink(decompressed_path)

    def test_compression_reduces_size(self):
        """Test that compression actually reduces file size for repetitive text."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        # Highly repetitive text should compress well
        test_text = "A" * 100 + "B" * 50 + "C" * 25
        temp_file.write(test_text)
        temp_file.close()
        
        original_size = os.path.getsize(temp_file.name)
        
        h = HuffmanCoding(temp_file.name)
        compressed_path = h.compress()
        compressed_size = os.path.getsize(compressed_path)
        
        # Compressed should be smaller than original
        assert compressed_size < original_size
        
        # Test decompression
        decompressed_path = h.decompress(compressed_path)
        
        # Cleanup
        os.unlink(temp_file.name)
        os.unlink(compressed_path)
        os.unlink(decompressed_path)
