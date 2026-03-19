def get_bit_width(dictionary_size):
    # Calculate the number of bits needed to represent the current dictionary size.
    
    bits = 1
    max_value = dictionary_size - 1
    while (2 ** bits) <= max_value:
        bits += 1
    
    # Minimum 9 bits needed
    if bits < 9:
        bits = 9
    return bits


def pack_codes_to_bytes(codes):
    # Pack integer codes into a variable-width bitstream and convert to bytes.

    bit_string = ""
    dictionary_size = 256  # Start with ASCII table
    
    for code in codes:
        width = get_bit_width(dictionary_size)
        code_binary = bin(code)[2:]
        code_binary = code_binary.zfill(width)
        bit_string += code_binary
        dictionary_size += 1
    
    padding = (8 - len(bit_string) % 8) % 8
    bit_string += '0' * padding
    
    result = bytearray([padding])
    
    for i in range(0, len(bit_string), 8):
        byte = bit_string[i:i+8]
        result.append(int(byte, 2))
    
    return result


def unpack_bytes_to_codes(packed_data):
    # Unpack bytes back into integer codes using variable-width decoding.

    padding = packed_data[0]

    bit_string = ""
    for byte in packed_data[1:]:
        byte_binary = bin(byte)[2:]
        byte_binary = byte_binary.zfill(8)
        bit_string += byte_binary

    if padding > 0:
        bit_string = bit_string[:-padding]

    codes = []
    dictionary_size = 256
    pos = 0
    
    while pos < len(bit_string):
        width = get_bit_width(dictionary_size)
        if pos + width > len(bit_string):
            break

        code_bits = bit_string[pos:pos+width]
        code = int(code_bits, 2)
        codes.append(code)
        
        pos += width
        dictionary_size += 1
    
    return codes


def compress(data):
    # Compress data using LZW algorithm with variable-width bitpacking.

    dictionary_size = 256
    dictionary = {}
    for i in range(dictionary_size):
        dictionary[chr(i)] = i
    
    codes = []
    current_string = ""
    
    for char in data:
        combined = current_string + char
        if combined in dictionary:
            current_string = combined
        else:
            codes.append(dictionary[current_string])
            dictionary[combined] = dictionary_size
            dictionary_size += 1
            current_string = char
    
    if current_string:
        codes.append(dictionary[current_string])
    
    return pack_codes_to_bytes(codes)


def decompress(compressed):
    # Decompress data using LZW algorithm with variable-width bitpacking.

    codes = unpack_bytes_to_codes(compressed)
    
    dictionary_size = 256
    dictionary = {}
    for i in range(dictionary_size):
        dictionary[i] = chr(i)
    
    result = []
    
    previous = chr(codes[0])
    result.append(previous)
    
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dictionary_size:
            entry = previous + previous[0]
        else:
            raise ValueError(f"Bad compressed code: {code}")
        
        result.append(entry)
        
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
