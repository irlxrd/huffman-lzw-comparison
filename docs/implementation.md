# Implementation Document


# High-Level Architecture and Module Descriptions

# 1. `huffman.py` - Huffman Coding Implementation

**Class**: `HuffmanCoding`

**Key Methods**:
- `make_frequency_dict(text)`: Analyzes character frequencies (O(n))
- `make_heap(frequency)`: Builds min-heap from frequencies (O(k log k))
- `merge_nodes()`: Constructs Huffman tree (O(k log k))
- `make_codes()`: Generates binary codes from tree (O(k))
- `compress()`: Main compression pipeline (O(n log n))
- `decompress(input_path)`: Decompression pipeline (O(n))

**Internal Class**: `HeapNode`
- Represents tree nodes with frequency, character, and left/right children
- Implements comparison operators for heap operations

**Data Flow**:
```
Input Text → Frequency Analysis → Min-Heap → Huffman Tree → 
Code Generation → Encoding → Padding → Byte Array → File
```

# 2. `lzw.py` - LZW Compression Implementation

**Functions**:
- `compress(data)`: Compresses text using LZW (O(n))
- `decompress(compressed)`: Decompresses LZW codes (O(n))

**Dictionary Management**:
- Initialized with ASCII characters (0-255)
- Dynamically expanded during compression
- Reconstructed during decompression (no storage needed)

**Data Flow**:
```
Input Text → Pattern Matching → Dictionary Building → 
Code Generation → Integer Array

Integer Array → Code Lookup → Dictionary Reconstruction → 
Text Reconstruction
```

# 3. `tests/test_performance.py` - Performance Benchmark

**Main Test**:
- `test_natural_text_performance_by_size()`: Runs Huffman and LZW on the same natural-language inputs and compares runtime and compression ratio.

**Input Source**:
- Uses `wiki_*` files from the project root as a text corpus.
- Benchmarks: `1 kB`, `4 kB`, `16 kB`, `64 kB`, `256 kB`, `1 MB`, `4 MB`, `16 MB`.

**Metrics**:
- Compression ratio (`compressed_size / original_size`)
- Runtime per algorithm
- Round-trip validation (decompressed text must match original)

**Execution**:
- Works with `pytest tests/test_performance.py`
- Works as a script: `python tests/test_performance.py`

# 4. `ui.py` - User Interface

**Features**:
- Interactive menu using Rich library
- File input or direct text input
- Side-by-side algorithm comparison
- Formatted output with tables and progress indicators

# Use of AI tools
- Claude Sonnet 4.5 was used for documentation and debugging. Also with UI implementation to make it prettier.
