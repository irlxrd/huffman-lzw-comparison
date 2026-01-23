import time
import sys
from huffman import HuffmanCoding
from lzw import compress as lzw_compress, decompress as lzw_decompress


def test_huffman(text):
    """Test Huffman coding and return statistics."""
    # Create a temporary file for Huffman (it requires file-based operation)
    temp_file = "temp_test.txt"
    with open(temp_file, 'w') as f:
        f.write(text)
    
    # Compress
    start_time = time.time()
    h = HuffmanCoding(temp_file)
    frequency = h.make_frequency_dict(text)
    h.make_heap(frequency)
    h.merge_nodes()
    h.make_codes()
    encoded_text = h.get_encoded_text(text)
    padded_encoded_text = h.pad_encoded_text(encoded_text)
    b = h.get_byte_array(padded_encoded_text)
    compress_time = time.time() - start_time
    
    # Calculate sizes
    original_size = len(text)
    compressed_size = len(b)
    
    # Clean up
    import os
    os.remove(temp_file)
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': (1 - compressed_size / original_size) * 100,
        'compress_time': compress_time,
        'bits_per_char': len(encoded_text) / original_size
    }


def test_lzw(text):
    """Test LZW compression and return statistics."""
    # Compress
    start_time = time.time()
    compressed = lzw_compress(text)
    compress_time = time.time() - start_time
    
    # Decompress to verify
    start_decompress = time.time()
    decompressed = lzw_decompress(compressed)
    decompress_time = time.time() - start_decompress
    
    # Calculate sizes (each code is typically 2 bytes)
    original_size = len(text)
    compressed_size = len(compressed) * 2  # 2 bytes per code
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': (1 - compressed_size / original_size) * 100,
        'compress_time': compress_time,
        'decompress_time': decompress_time,
        'codes_count': len(compressed),
        'match': text == decompressed
    }


def print_statistics(algorithm, stats):
    """Print statistics for an algorithm."""
    print(f"\n{'='*60}")
    print(f"{algorithm} Statistics")
    print(f"{'='*60}")
    print(f"Original Size:      {stats['original_size']:>10} bytes")
    print(f"Compressed Size:    {stats['compressed_size']:>10} bytes")
    print(f"Compression Ratio:  {stats['compression_ratio']:>10.2f}%")
    print(f"Compress Time:      {stats['compress_time']:>10.6f} seconds")
    
    if 'decompress_time' in stats:
        print(f"Decompress Time:    {stats['decompress_time']:>10.6f} seconds")
    if 'bits_per_char' in stats:
        print(f"Bits per Character: {stats['bits_per_char']:>10.2f}")
    if 'codes_count' in stats:
        print(f"Number of Codes:    {stats['codes_count']:>10}")
    if 'match' in stats:
        print(f"Decompression OK:   {stats['match']}")


def compare_algorithms(test_data):
    """Compare both algorithms on the same data."""
    print("\n" + "="*60)
    print("COMPRESSION ALGORITHM COMPARISON")
    print("="*60)
    print(f"\nTest Data: {test_data[:50]}{'...' if len(test_data) > 50 else ''}")
    print(f"Data Length: {len(test_data)} characters")
    
    # Test Huffman
    print("\n[Testing Huffman Coding...]")
    huffman_stats = test_huffman(test_data)
    print_statistics("HUFFMAN CODING", huffman_stats)
    
    # Test LZW
    print("\n[Testing LZW Compression...]")
    lzw_stats = test_lzw(test_data)
    print_statistics("LZW COMPRESSION", lzw_stats)
    
    # Comparison
    print(f"\n{'='*60}")
    print("COMPARISON")
    print(f"{'='*60}")
    
    if huffman_stats['compression_ratio'] > lzw_stats['compression_ratio']:
        winner = "Huffman"
        diff = huffman_stats['compression_ratio'] - lzw_stats['compression_ratio']
    else:
        winner = "LZW"
        diff = lzw_stats['compression_ratio'] - huffman_stats['compression_ratio']
    
    print(f"Better Compression:  {winner} (by {diff:.2f}%)")
    print(f"Huffman Time:        {huffman_stats['compress_time']:.6f}s")
    print(f"LZW Time:            {lzw_stats['compress_time']:.6f}s")
    
    if huffman_stats['compress_time'] < lzw_stats['compress_time']:
        faster = "Huffman"
        time_diff = lzw_stats['compress_time'] - huffman_stats['compress_time']
    else:
        faster = "LZW"
        time_diff = huffman_stats['compress_time'] - lzw_stats['compress_time']
    
    print(f"Faster Algorithm:    {faster} (by {time_diff:.6f}s)")
    print(f"{'='*60}\n")


def main():

    print("\n" + "="*60)
    choice = input("Please enter text to compress: ")
    if choice:
        compare_algorithms(choice)

if __name__ == "__main__":
    main()
