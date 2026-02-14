#!/usr/bin/env python3
import time
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.text import Text
from rich import box
from src.huffman import HuffmanCoding
from src.lzw import compress as lzw_compress, decompress as lzw_decompress

console = Console()


def test_huffman(text):
    """Test Huffman coding and return statistics."""
    temp_file = "temp_test.txt"
    with open(temp_file, 'w') as f:
        f.write(text)
    
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
    
    original_size = len(text)
    compressed_size = len(b)
    
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
    start_time = time.time()
    compressed = lzw_compress(text)
    compress_time = time.time() - start_time
    
    start_decompress = time.time()
    decompressed = lzw_decompress(compressed)
    decompress_time = time.time() - start_decompress
    
    original_size = len(text)
    compressed_size = len(compressed) * 2
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'compression_ratio': (1 - compressed_size / original_size) * 100,
        'compress_time': compress_time,
        'decompress_time': decompress_time,
        'codes_count': len(compressed),
        'match': text == decompressed
    }


def create_stats_table(huffman_stats, lzw_stats):
    """Create a comparison table with both algorithms."""
    table = Table(title="📊 Compression Statistics", box=box.ROUNDED, show_header=True, header_style="bold magenta")
    
    table.add_column("Metric", style="cyan", justify="left")
    table.add_column("Huffman Coding", style="green", justify="right")
    table.add_column("LZW Compression", style="yellow", justify="right")
    table.add_column("Winner", style="bold red", justify="center")
    
    # Original Size
    table.add_row(
        "Original Size",
        f"{huffman_stats['original_size']} bytes",
        f"{lzw_stats['original_size']} bytes",
        "—"
    )
    
    # Compressed Size
    winner = "Huffman" if huffman_stats['compressed_size'] < lzw_stats['compressed_size'] else "LZW"
    table.add_row(
        "Compressed Size",
        f"{huffman_stats['compressed_size']} bytes",
        f"{lzw_stats['compressed_size']} bytes",
        winner
    )
    
    # Compression Ratio
    winner = "Huffman" if huffman_stats['compression_ratio'] > lzw_stats['compression_ratio'] else "LZW"
    table.add_row(
        "Compression Ratio",
        f"{huffman_stats['compression_ratio']:.2f}%",
        f"{lzw_stats['compression_ratio']:.2f}%",
        winner
    )
    
    # Compression Time
    winner = "Huffman" if huffman_stats['compress_time'] < lzw_stats['compress_time'] else "LZW"
    table.add_row(
        "Compression Time",
        f"{huffman_stats['compress_time']:.6f}s",
        f"{lzw_stats['compress_time']:.6f}s",
        winner
    )
    
    # Additional metrics
    table.add_row(
        "Bits per Character",
        f"{huffman_stats['bits_per_char']:.2f}",
        f"{(lzw_stats['compressed_size'] * 8) / lzw_stats['original_size']:.2f}",
        "—"
    )
    
    return table


def show_welcome():
    """Display welcome screen."""
    console.clear()
    console.print("\n[bold white]COMPRESSION ALGORITHMS COMPARISON[/bold white]")
    console.print("[bold blue]Huffman Coding vs LZW[/bold blue]")
    console.print()


def show_menu():
    """Display main menu and get user choice."""
    console.print("\n[bold cyan]=== Main Menu ===[/bold cyan]")
    console.print("1. Enter text manually")
    console.print("2. Load from file")
    console.print("3. Run test cases")
    console.print("4. Exit")
    console.print()
    
    choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])
    return choice


def get_text_input():
    """Get text input from user."""
    console.print("\n[bold yellow]Enter or paste your text[/bold yellow] (press Ctrl+D or Ctrl+Z when done):")
    console.print("[dim]Tip: You can paste multi-line text[/dim]\n")
    
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    return '\n'.join(lines)


def load_from_file():
    """Load text from a file."""
    filepath = Prompt.ask("\n[bold yellow]Enter file path[/bold yellow]")
    
    try:
        with open(filepath, 'r') as f:
            text = f.read()
        console.print(f"[green]✓[/green] Loaded {len(text)} characters from {filepath}")
        return text
    except FileNotFoundError:
        console.print(f"[red]✗[/red] File not found: {filepath}")
        return None
    except Exception as e:
        console.print(f"[red]✗[/red] Error reading file: {e}")
        return None


def run_comparison(text, show_text=True):
    """Run compression comparison with progress indicators."""
    if show_text:
        preview = text[:100] + "..." if len(text) > 100 else text
        console.print(Panel(
            f"[dim]{preview}[/dim]",
            title=f"Input Text ({len(text)} characters)",
            border_style="blue"
        ))
        console.print()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Test Huffman
        task1 = progress.add_task("[green]Testing Huffman Coding...", total=None)
        huffman_stats = test_huffman(text)
        progress.update(task1, completed=True)
        progress.stop_task(task1)
        
        # Test LZW
        task2 = progress.add_task("[yellow]Testing LZW Compression...", total=None)
        lzw_stats = test_lzw(text)
        progress.update(task2, completed=True)
        progress.stop_task(task2)
    
    console.print()
    
    # Display results
    table = create_stats_table(huffman_stats, lzw_stats)
    console.print(table)
    
    # Show winner summary
    console.print()
    if huffman_stats['compression_ratio'] > lzw_stats['compression_ratio']:
        diff = huffman_stats['compression_ratio'] - lzw_stats['compression_ratio']
        console.print(Panel(
            f"[bold green]Huffman Coding[/bold green] achieved better compression by [bold]{diff:.2f}%[/bold]",
            title="Winner",
            border_style="green"
        ))
    else:
        diff = lzw_stats['compression_ratio'] - huffman_stats['compression_ratio']
        console.print(Panel(
            f"[bold yellow]LZW Compression[/bold yellow] achieved better compression by [bold]{diff:.2f}%[/bold]",
            title="Winner",
            border_style="yellow"
        ))


def run_test_cases():
    """Run predefined test cases."""
    test_cases = [
        {
            'name': 'Repeated Pattern',
            'data': 'TOBEORNOTTOBEORTOBEORNOT' * 45,
            'description': 'Test case with pattern repetition'
        },
        {
            'name': 'Lorem Ipsum',
            'data': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' * 5,
            'description': 'Natural language text with moderate repetition'
        },
        {
            'name': 'DNA Sequence',
            'data': 'ATCGATCGATCGATCGTAGCTAGCTAGCTAGCTACGTACGTACGTACGT' * 10,
            'description': 'Biological sequence data with high pattern frequency'
        },
        {
            'name': 'Code Sample',
            'data': '''def function():
    for i in range(10):
        print(i)
    return True
''' * 10,
            'description': 'Source code with structured repetition'
        }
    ]
    
    console.print(f"\n[bold cyan]Available Test Cases:[/bold cyan]")
    for i, test in enumerate(test_cases, 1):
        console.print(f"{i}. [yellow]{test['name']}[/yellow] - {test['description']}")
    console.print(f"{len(test_cases) + 1}. [green]Run all test cases[/green]")
    console.print()
    
    choice = Prompt.ask(
        "Select a test case",
        choices=[str(i) for i in range(1, len(test_cases) + 2)]
    )
    
    if choice == str(len(test_cases) + 1):
        # Run all tests
        for test in test_cases:
            console.print(f"\n[bold magenta]{'═' * 60}[/bold magenta]")
            console.print(f"[bold magenta]Test Case: {test['name']}[/bold magenta]")
            console.print(f"[dim]{test['description']}[/dim]")
            console.print(f"[bold magenta]{'═' * 60}[/bold magenta]\n")
            run_comparison(test['data'], show_text=False)
            console.print()
            if test != test_cases[-1]:
                input("Press Enter to continue to next test...")
    else:
        # Run selected test
        test = test_cases[int(choice) - 1]
        console.print(f"\n[bold magenta]{'═' * 60}[/bold magenta]")
        console.print(f"[bold magenta]Test Case: {test['name']}[/bold magenta]")
        console.print(f"[dim]{test['description']}[/dim]")
        console.print(f"[bold magenta]{'═' * 60}[/bold magenta]\n")
        run_comparison(test['data'])


def main():
    """Main application loop."""
    show_welcome()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            text = get_text_input()
            if text.strip():
                run_comparison(text)
            else:
                console.print("[red]✗[/red] No text entered")
        
        elif choice == "2":
            text = load_from_file()
            if text:
                run_comparison(text)
        
        elif choice == "3":
            run_test_cases()
        
        elif choice == "4":
            console.print("\n[bold blue]Thanks for using the compression tool![/bold blue]\n")
            break
        
        console.print()
        if not Confirm.ask("Would you like to continue?"):
            console.print("\n[bold blue]Thanks for using the compression tool![/bold blue]\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Interrupted by user[/bold red]")
        console.print("[bold blue]Goodbye![/bold blue]\n")
