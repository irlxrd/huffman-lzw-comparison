# Testing Documentation

## Test Structure

- **test_huffman.py**: 14 tests for Huffman coding (frequency analysis, heap operations, tree construction, encoding/decoding, end-to-end)
- **test_lzw.py**: 19 tests for LZW compression (compression, decompression, round-trip cycles, edge cases)
- **test_performance.py**: 1 benchmark-style test that compares Huffman and LZW on natural-language corpus data
- **Total**: 34 tests

## Performance Test (`test_performance.py`)

- Uses natural text from `wiki_*` files in the project root.
- Runs both algorithms on the same inputs and verifies round-trip correctness.
- Reports compression ratio and runtime for each size.
- Size set: `1 kB`, `4 kB`, `16 kB`, `64 kB`, `256 kB`, `1 MB`, `4 MB`, `16 MB`.
- If requested size exceeds corpus bytes, the corpus is repeated to reach target size.

## Coverage

```
Name                Stmts   Miss  Cover
-----------------------------------------
src/huffman.py        115      3    97%
src/lzw.py             47     12    74%
-----------------------------------------
TOTAL                 418    270    35%
```

- **Huffman**: 97% coverage (missing: error edge cases)
- **LZW**: 74% coverage (missing: main function)


## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_huffman.py
pytest tests/test_lzw.py
pytest tests/test_performance.py

# Run performance test directly (prints benchmark table)
python tests/test_performance.py

# With coverage
pytest --cov=src --cov-report=html
```
