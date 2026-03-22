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

        assert len(h.heap) == 3
        assert h.heap[0].freq == 1
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

        assert len(h.heap) == 1
        assert h.heap[0].freq == 6
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

        assert len(h.codes) == 3
        assert 'A' in h.codes
        assert 'B' in h.codes
        assert 'C' in h.codes

        assert len(h.codes['A']) <= len(h.codes['C'])

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

        assert all(c in '01' for c in encoded)
        assert len(encoded) > 0
        os.unlink(temp_file.name)

    def test_pad_encoded_text(self):
        """Test padding of encoded text to byte boundary."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)

        encoded = "001"
        padded = h.pad_encoded_text(encoded)

        assert len(padded) % 8 == 0
        padding_info = int(padded[:8], 2)
        assert padding_info == 5
        os.unlink(temp_file.name)

    def test_get_byte_array(self):
        """Test conversion of binary string to byte array."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)

        padded_text = "0100101001100001"
        byte_array = h.get_byte_array(padded_text)
        
        assert len(byte_array) == 2
        assert byte_array[0] == int("01001010", 2)
        assert byte_array[1] == int("01100001", 2)
        os.unlink(temp_file.name)

    def test_get_byte_array_invalid_length(self):
        """Test that byte array conversion fails with invalid length."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        temp_file.write("test")
        temp_file.close()
        
        h = HuffmanCoding(temp_file.name)

        invalid_text = "0100101"
        with pytest.raises(ValueError):
            h.get_byte_array(invalid_text)
        os.unlink(temp_file.name)

    def test_heap_node_comparison(self):
        """Test HeapNode comparison operators."""
        node1 = HuffmanCoding.HeapNode('A', 5)
        node2 = HuffmanCoding.HeapNode('B', 3)
        node3 = HuffmanCoding.HeapNode('C', 5)

        assert node2 < node1
        assert not (node1 < node2)

        assert node1 == node3
        assert not (node1 == node2)

    def test_compress_decompress_simple(self):
        """Test end-to-end compression and decompression with simple text."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        test_text = "AAABBBCCCDDD"
        temp_file.write(test_text)
        temp_file.close()

        h = HuffmanCoding(temp_file.name)
        compressed_path = h.compress()

        assert os.path.exists(compressed_path)
        compressed_size = os.path.getsize(compressed_path)
        assert compressed_size > 0

        decompressed_path = h.decompress(compressed_path)

        with open(decompressed_path, 'r') as f:
            decompressed_text = f.read()
        
        assert decompressed_text == test_text

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

        os.unlink(temp_file.name)
        os.unlink(compressed_path)
        os.unlink(decompressed_path)

    def test_compression_reduces_size(self):
        """Test that compression actually reduces file size for repetitive text."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        test_text = "A" * 100 + "B" * 50 + "C" * 25
        temp_file.write(test_text)
        temp_file.close()
        
        original_size = os.path.getsize(temp_file.name)
        
        h = HuffmanCoding(temp_file.name)
        compressed_path = h.compress()
        compressed_size = os.path.getsize(compressed_path)

        assert compressed_size < original_size

        decompressed_path = h.decompress(compressed_path)

        os.unlink(temp_file.name)
        os.unlink(compressed_path)
        os.unlink(decompressed_path)
