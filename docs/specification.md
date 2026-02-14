# Specification Document

## Project Information

**Project Name**: Huffman-LZW Compression Tool  
**Programming Language**: Python (3.10+)  
**Study Program**: [Bachelor's of Science (Computer & Data Science)]  

## Peer Review Languages

I am proficient in the following programming languages:
- Python
- C
- Java


## Project Overview

### Problem Being Solved

This project implements and compares two fundamental lossless data compression algorithms: **Huffman Coding** and **Lempel-Ziv-Welch (LZW)**. The goal is to:

1. Implement both algorithms from scratch
2. Compare their compression efficiency on various file sizes
3. Measure and analyze their performance characteristics
4. Provide a user-friendly tool for practical compression tasks

### Core of the Project

**The core of this project is the implementation of two lossless compression algorithms:**

1. **Huffman Coding**: A greedy algorithm that builds an optimal prefix-free binary code based on character frequency analysis. It uses a priority queue (min-heap) to construct a binary tree where frequent characters have shorter codes.

2. **LZW Compression**: A dictionary-based algorithm that replaces repeated sequences with shorter codes. It dynamically builds a dictionary during compression and reconstructs it during decompression without needing to store the dictionary.


## Algorithms and Data Structures

### Algorithms Implemented

1. **Huffman Coding**
   - Frequency analysis
   - Min-heap construction
   - Huffman tree building through node merging
   - Variable-length code generation
   - Binary encoding/decoding

2. **LZW Compression**
   - Dictionary initialization (ASCII 0-255)
   - Pattern recognition and dictionary building
   - Code generation and output
   - Dictionary reconstruction during decompression

### Data Structures Used

1. **Min-Heap (Priority Queue)**
   - Used in: Huffman coding
   - Purpose: Efficiently select two nodes with minimum frequency
   - Implementation: Python's `heapq` module

2. **Binary Tree**
   - Used in: Huffman coding
   - Purpose: Store character-to-code mapping
   - Implementation: Custom `HeapNode` class with left/right children

3. **Dictionary (Hash Map)**
   - Used in: Both algorithms
   - Purpose: 
     - Huffman: Store character frequencies and code mappings
     - LZW: Store string-to-code mappings (compression) and code-to-string mappings (decompression)
   - Implementation: Python's built-in `dict`

4. **Byte Array**
   - Used in: Huffman coding
   - Purpose: Store compressed binary data efficiently
   - Implementation: Python's `bytearray`

## Input and Usage

### Program Inputs

1. **Text Files**
   - Format: Plain text (UTF-8 or ASCII)
   - Size: Any size (tested up to 10 MB)
   - Content: Natural language text, code, or any text-based data

2. **Compressed Files**
   - Format: `.bin` files (for Huffman decompression)
   - Format: Integer arrays (for LZW decompression)

### How Inputs Are Used

**Huffman Coding:**
```python
# Compression
h = HuffmanCoding("input.txt")
compressed = h.compress()  # Creates input.bin

# Decompression
decompressed = h.decompress("input.bin")  # Creates input_decompressed.txt
```

**LZW Compression:**
```python
# Compression
compressed_codes = lzw_compress(text_string)

# Decompression
original_text = lzw_decompress(compressed_codes)
```

## Time and Space Complexity Analysis

### Huffman Coding

**Time Complexity:**
- **Compression**: O(n log n)
  - Frequency counting: O(n) where n = text length
  - Heap operations: O(k log k) where k = unique characters
  - Tree traversal for code generation: O(k)
  - Text encoding: O(n)
  - Overall: O(n + k log k) ≈ O(n log n) when k is proportional to input size
  
- **Decompression**: O(n)
  - Reading compressed file: O(m) where m = compressed size
  - Decoding using code tree: O(n) where n = original text length
  - Overall: O(n)

**Space Complexity:**
- **Compression**: O(k)
  - Frequency dictionary: O(k)
  - Min-heap: O(k)
  - Code mapping: O(k)
  - Where k = number of unique characters
  
- **Decompression**: O(k + n)
  - Reverse mapping: O(k)
  - Output text: O(n)

**Why these complexities?**
- Heap operations (insert/extract-min) take O(log k) time
- We perform k-1 merge operations to build the tree
- Each character in the input is processed once during encoding
- Huffman tree depth is at most k, making code lookup efficient

### LZW Compression

**Time Complexity:**
- **Compression**: O(n)
  - Single pass through input: O(n)
  - Dictionary lookup: O(1) average (hash table)
  - Dictionary insertion: O(1) average
  - Overall: O(n)
  
- **Decompression**: O(n)
  - Single pass through compressed codes: O(m) where m = number of codes
  - Dictionary lookup: O(1) average
  - Dictionary insertion: O(1) average
  - Output generation: O(n)
  - Overall: O(n)

**Space Complexity:**
- **Compression**: O(k)
  - Dictionary size grows with pattern discovery
  - Maximum dictionary size: typically limited (e.g., 2^12 or 4096 entries)
  - Where k = number of dictionary entries
  
- **Decompression**: O(k + n)
  - Dictionary: O(k)
  - Output: O(n)

**Why these complexities?**
- Hash table provides O(1) average lookup/insert
- Single pass through data (no backtracking needed)
- Dictionary size is bounded, preventing exponential growth
- LZW is more efficient than Huffman for highly repetitive data

## Expected Performance Characteristics

### Compression Ratio

**Huffman:**
- Best case: Text with highly skewed character distribution (50-60% reduction)
- Worst case: Text with uniform character distribution (minimal reduction)
- Performs well on: Natural language text, code files

**LZW:**
- Best case: Highly repetitive text (60-80% reduction)
- Worst case: Random data (may expand data)
- Performs well on: Repetitive patterns, structured data


## Project Scope

The implementation includes:

- Full Huffman coding (compression and decompression)
- Full LZW compression (compression and decompression)
- Comparison framework with performance metrics
- User interface for interactive testing
- Comprehensive test suite

