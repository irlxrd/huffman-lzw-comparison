def compress(data):
    """
    Compress data using LZW algorithm.
    """
    # Initializing a dictionary with all ASCII values
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    
    result = []
    current_string = ""
    
    for char in data:
        combined = current_string + char
        if combined in dictionary:
            current_string = combined
        else:
            # Output the code for current_string
            result.append(dictionary[current_string])
            # Add combined to dictionary
            dictionary[combined] = dictionary_size
            dictionary_size += 1
            current_string = char
    
    # Output the code for remaining string
    if current_string:
        result.append(dictionary[current_string])
    
    return result


def decompress(compressed):
    """
    Decompress data using LZW algorithm.
    """
    # Initializing a dictionary with all ASCII values
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}
    
    result = []
    
    # Get first code
    previous = chr(compressed[0])
    result.append(previous)
    
    for code in compressed[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dictionary_size:
            # Special case: code not in dictionary yet
            entry = previous + previous[0]
        else:
            raise ValueError(f"Bad compressed code: {code}")
        
        result.append(entry)
        
        # Add previous + first char of entry to dictionary
        dictionary[dictionary_size] = previous + entry[0]
        dictionary_size += 1
        
        previous = entry
    
    return ''.join(result)


def main():
    # Example usage
    original = "ABcabcDABks"
    print(f"Original: {original}")
    print(f"Original size: {len(original)} characters")
    
    # Compress
    compressed = compress(original)
    print(f"\nCompressed: {compressed}")
    print(f"Compressed size: {len(compressed)} codes")
    
    # Calculate compression ratio
    compression_ratio = (1 - len(compressed) / len(original)) * 100
    print(f"Compression ratio: {compression_ratio:.2f}%")
    
    # Decompress
    decompressed = decompress(compressed)
    print(f"\nDecompressed: {decompressed}")
    print(f"Match: {original == decompressed}")


if __name__ == "__main__":
    main()
