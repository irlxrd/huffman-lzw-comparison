# Compression Tool

A Python tool to compare Huffman and LZW compression algorithms with an interactive UI.

## Features

- **Huffman Coding**: Optimal prefix-free encoding based on character frequency
- **LZW Compression**: Dictionary-based compression algorithm
- **Interactive UI**: Rich terminal interface for easy comparison
- **Performance Metrics**: Compare compression ratios and execution times

## Requirements

- Python 3.10 or higher
- Dependencies listed in `pyproject.toml`

## Installation & Setup

### Option 1: Using Poetry (Recommended)

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd compression
   ```

2. **Install Poetry**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**
   ```bash
   poetry install
   ```

4. **Run the UI**
   ```bash
   poetry run python -m src.ui
   ```

### Option 2: Using pip

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd compression
   ```

2. **Install dependencies**
   ```bash
   pip install rich
   ```

3. **Run the UI from the project root**
   ```bash
   python3 -m src.ui
   ```

## Important: Running the Application

**Always run the application from the project root directory** using the module syntax:

```bash
# Correct way - from the project root
cd /path/to/compression
python3 -m src.ui
```

**Do NOT run it like this:**
```bash
# Wrong - will cause import errors
python src/ui.py
python3 src/ui.py
```

### Why?

The project uses absolute imports (e.g., `from src.huffman import ...`). Python needs to recognize `src` as a package, which only works when:
1. You're in the project root directory
2. You use the `-m` flag to run it as a module


## Running Tests

```bash
# Using poetry
poetry run pytest

# Using pytest directly
pytest

# With coverage report
pytest --cov=src --cov-report=html
```

## Project Structure

```
compression/
├── src/                 # Main package directory
│   ├── __init__.py     # Package initialization
│   ├── huffman.py      # Huffman coding implementation
│   ├── lzw.py          # LZW compression implementation
│   └── ui.py           # Interactive terminal UI
├── tests/              # Test files
│   ├── test_huffman.py
│   └── test_lzw.py
├── docs/               # Documentation
├── pyproject.toml      # Project configuration and dependencies
└── README.md           # This file
```

## Usage

1. **Launch the interactive UI**:
   ```bash
   python3 -m src.ui
   ```

## Documentation

- [Implementation Details](docs/implementation.md)
- [Specification](docs/specification.md)
- [Testing Documentation](docs/testing.md)
- [Weekly Report](docs/weekly-report.md)

