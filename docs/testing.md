# Testing Documentation

## Test Structure

- **test_huffman.py**: 14 tests for Huffman coding (frequency analysis, heap operations, tree construction, encoding/decoding, end-to-end)
- **test_lzw.py**: 19 tests for LZW compression (compression, decompression, round-trip cycles, edge cases)
- **Total**: 33 tests

## Coverage

```
Name                Stmts   Miss  Cover
-----------------------------------------
src/huffman.py        115      3    97%
src/lzw.py             47     12    74%
src/comparison.py      86     86     0%
src/ui.py             169    169     0%
-----------------------------------------
TOTAL                 418    270    35%
```

- **Huffman**: 97% coverage (missing: error edge cases)
- **LZW**: 74% coverage (missing: main function)
- **UI/Comparison**: 0% (not tested yet)

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_huffman.py
pytest tests/test_lzw.py

# With coverage
pytest --cov=src --cov-report=html
```
