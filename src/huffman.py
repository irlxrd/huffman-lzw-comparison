import heapq
import os


class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []  # Min-heap to build Huffman tree
		self.codes = {}  # Dictionary mapping characters to their binary codes
		self.reverse_mapping = {}  # Dictionary mapping binary codes back to characters

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if other is None:
				return False
			if not isinstance(other, HuffmanCoding.HeapNode):
				return False
			return self.freq == other.freq

	# Functions for compression:

	def make_frequency_dict(self, text):
		# Calculate frequency of each character in the text and return as a dict.

		frequency = {}
		for character in text:
			if character in frequency:
				frequency[character] += 1
			else:
				frequency[character] = 1
		return frequency

	def make_heap(self, frequency):
		# Make priority queue (min-heap) from frequency dict.

		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		# Build Huffman tree by repeatedly merging nodes with lowest frequencies.

		while len(self.heap) > 1:
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1   # Left child (will represent '0' in code)
			merged.right = node2  # Right child (will represent '1' in code)

			heapq.heappush(self.heap, merged) 


	def make_codes_helper(self, root, current_code):
		# Recursively generate Huffman codes by traversing the tree.

		if root is None:
			return

		if root.char is not None:
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		#Generate Huffman codes for all characters in the tree.

		root = heapq.heappop(self.heap)
		self.make_codes_helper(root, "")


	def get_encoded_text(self, text):
		# Replace each character in text with its Huffman code.
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		# Pad encoded text to make its length a multiple of 8 bits (1 byte).

		BITS_PER_BYTE = 8
		extra_padding = (BITS_PER_BYTE - len(encoded_text) % BITS_PER_BYTE) % BITS_PER_BYTE
		
		encoded_text += "0" * extra_padding

		padded_info = bin(extra_padding)[2:]
		padded_info = padded_info.zfill(8)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		# Convert binary string into byte array for file storage.
  
		BITS_PER_BYTE = 8
		if len(padded_encoded_text) % BITS_PER_BYTE != 0:
			raise ValueError("Encoded text not padded properly")

		byte_array = []
		for i in range(0, len(padded_encoded_text), BITS_PER_BYTE):
			eight_bits = padded_encoded_text[i:i + BITS_PER_BYTE]
			byte_value = int(eight_bits, 2)
			byte_array.append(byte_value)
		return bytearray(byte_array)


	def compress(self):
		# Main compression method that orchestrates the entire Huffman encoding process.

		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"

		with open(self.path, 'r') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			# Step 1: Analyze character frequencies
			frequency = self.make_frequency_dict(text)
			# Step 2: Create min-heap with leaf nodes
			self.make_heap(frequency)
			# Step 3: Build Huffman tree by merging nodes
			self.merge_nodes()
			# Step 4: Generate binary codes from tree
			self.make_codes()
			# Step 5: Encode the text using generated codes
			encoded_text = self.get_encoded_text(text)
			# Step 6: Pad to make length divisible by 8
			padded_encoded_text = self.pad_encoded_text(encoded_text)
			# Step 7: Convert bit string to bytes
			b = self.get_byte_array(padded_encoded_text)
			# Write compressed bytes to output file
			output.write(bytes(b))

		print("Compressed")
		return output_path

	# Functions for decompression:

	def remove_padding(self, padded_encoded_text):
		#Remove padding from encoded text.

		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-extra_padding] if extra_padding > 0 else padded_encoded_text

		return encoded_text

	def decode_text(self, encoded_text):
        #Decode binary string back to original text using reverse mapping.
	
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			# Check if current code matches any character
			if current_code in self.reverse_mapping:
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""  # Reset for next character

		return decoded_text

	def decompress(self, input_path):
		# Main decompression method that reverses the Huffman encoding process.
	
		filename = input_path.replace(".bin", "")
		output_path = filename + "_decompressed.txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:

			bit_string = ""
			byte = file.read(1)
			while byte:
				byte_value = byte[0]
				bits = bin(byte_value)[2:]
				bits = bits.zfill(8)
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)

			output.write(decompressed_text)

		print("Decompressed")
		return output_path


