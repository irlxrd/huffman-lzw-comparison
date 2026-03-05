import math


def get_bit_width(dictionary_size):
    """Calculate the number of bits needed to represent the current dictionary size.
    
    Args:
        dictionary_size: Current size of the dictionary
        
    Returns:
        Number of bits needed (minimum 9)
    """
    # Need enough bits to represent values from 0 to dictionary_size-1
    # Start with 9 bits minimum (for 256-511)
    return max(9, math.ceil(math.log2(dictionary_size)))


def pack_codes_to_bytes(codes):
    """Pack integer codes into a variable-width bitstream and convert to bytes.
    
    As the dictionary grows during compression, we use progressively more bits:
    - 256-511: 9 bits
    - 512-1023: 10 bits
    - 1024-2047: 11 bits
    - And so on...
    
    Args:
        codes: List of integer codes from LZW compression
        
    Returns:
        bytearray containing the packed compressed data
    """
    bit_string = ""
    dictionary_size = 256  # Start with ASCII table
    
    for code in codes:
        # Calculate current bit width based on dictionary size
        width = get_bit_width(dictionary_size)
        # Convert code to binary string with appropriate width
        bit_string += format(code, f'0{width}b')
        # Dictionary grows by 1 after each code output
        dictionary_size += 1
    
    # Pad to byte boundary
    padding = (8 - len(bit_string) % 8) % 8
    bit_string += '0' * padding
    
    # Store padding info in first byte
    result = bytearray([padding])
    
    # Convert bit string to bytes
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]
        result.append(int(byte, 2))
    
    return result


def unpack_bytes_to_codes(packed_data):
    """Unpack bytes back into integer codes using variable-width decoding.
    
    Args:
        packed_data: bytearray of compressed data
        
    Returns:
        List of integer codes
    """
    # First byte contains padding info
    padding = packed_data[0]
    
    # Convert remaining bytes to bit string
    bit_string = ""
    for byte in packed_data[1:]:
        bit_string += format(byte, '08b')
    
    # Remove padding from end
    if padding > 0:
        bit_string = bit_string[:-padding]
    
    # Decode variable-width codes
    codes = []
    dictionary_size = 256
    pos = 0
    
    while pos < len(bit_string):
        width = get_bit_width(dictionary_size)
        if pos + width > len(bit_string):
            break
        
        # Extract code of current width
        code_bits = bit_string[pos:pos+width]
        code = int(code_bits, 2)
        codes.append(code)
        
        pos += width
        dictionary_size += 1
    
    return codes


def compress(data):
    """Compress data using LZW algorithm with variable-width bitpacking.
    
    Args:
        data: String to compress
        
    Returns:
        bytearray containing compressed data
    """
    # Initializing a dictionary with all ASCII values
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    
    codes = []
    current_string = ""
    
    for char in data:
        combined = current_string + char
        if combined in dictionary:
            current_string = combined
        else:
            # Output the code for current_string
            codes.append(dictionary[current_string])
            # Add combined to dictionary
            dictionary[combined] = dictionary_size
            dictionary_size += 1
            current_string = char
    
    # Output the code for remaining string
    if current_string:
        codes.append(dictionary[current_string])
    
    # Pack codes into bytes
    return pack_codes_to_bytes(codes)


def decompress(compressed):
    """Decompress data using LZW algorithm with variable-width bitpacking.
    
    Args:
        compressed: bytearray of compressed data
        
    Returns:
        Original decompressed string
    """
    # Unpack bytes into codes
    codes = unpack_bytes_to_codes(compressed)
    
    # Initializing a dictionary with all ASCII values
    dictionary_size = 256
    dictionary = {i: chr(i) for i in range(dictionary_size)}
    
    result = []
    
    # Get first code
    previous = chr(codes[0])
    result.append(previous)
    
    for code in codes[1:]:
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
    original = "TOBEORNOTTOBEORTOBEORNOT"
    print(f"Original: {original}")
    print(f"Original size: {len(original)} bytes\n")
    
    # Compress
    compressed = compress(original)
    print(f"Compressed: {compressed.hex()}")
    print(f"Compressed size: {len(compressed)} bytes")
    
    # Calculate compression ratio
    compression_ratio = (1 - len(compressed) / len(original)) * 100
    print(f"Compression ratio: {compression_ratio:.2f}%\n")
    
    # Decompress
    decompressed = decompress(compressed)
    print(f"Decompressed: {decompressed}")
    print(f"Match: {original == decompressed}")

if __name__ == "__main__":
    main()
