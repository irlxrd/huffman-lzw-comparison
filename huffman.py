"""Huffman Coding Implementation for Text Compression

HUFFMAN CODING OVERVIEW:
Huffman coding is a lossless data compression algorithm that assigns variable-length
codes to characters based on their frequency of occurrence. Characters that appear
more frequently get shorter codes, while rare characters get longer codes.

KEY IDEA:
- Instead of using fixed-length codes (e.g., 8 bits per character in ASCII),
  use variable-length codes to save space
- Build a binary tree where frequent characters are closer to the root
- Each left edge represents '0', each right edge represents '1'
- The path from root to a leaf node gives that character's code

ALGORITHM STEPS:
1. Calculate frequency of each character
2. Create a min-heap with nodes for each character
3. Repeatedly merge two nodes with lowest frequencies
4. Build the Huffman tree bottom-up
5. Generate binary codes by traversing tree (left=0, right=1)
6. Encode text using generated codes
7. Convert bit string to bytes for storage
"""

import heapq
import os
from collections import Counter


class HuffmanCoding:
	"""Main class for Huffman encoding and decoding."""
	
	def __init__(self, path):
		"""Initialize the Huffman coding object.
		
		Args:
			path: Path to the file to be compressed
		"""
		self.path = path
		self.heap = []  # Min-heap to build Huffman tree
		self.codes = {}  # Dictionary mapping characters to their binary codes
		self.reverse_mapping = {}  # Dictionary mapping binary codes back to characters

	class HeapNode:
		"""Node structure for building the Huffman tree.
		
		Each node represents either:
		- A leaf node: contains a character and its frequency
		- An internal node: merge of two nodes, no character, combined frequency
		"""
		
		def __init__(self, char, freq):
			"""Create a new tree node.
			
			Args:
				char: The character (None for internal nodes)
				freq: Frequency/weight of this node
			"""
			self.char = char  # Character stored (None for merged nodes)
			self.freq = freq  # Frequency count for this character/subtree
			self.left = None  # Left child (represents '0' in code)
			self.right = None  # Right child (represents '1' in code)

		# Defining comparators for heap operations
		# The heap needs to compare nodes by frequency to maintain min-heap property
		def __lt__(self, other):
			"""Less than comparison based on frequency. Python calls this when heappush() or heappop() is used."""
			return self.freq < other.freq

		def __eq__(self, other):
			"""Equality comparison based on frequency."""
			if other is None:
				return False
			if not isinstance(other, HuffmanCoding.HeapNode):
				return False
			return self.freq == other.freq

	# Functions for compression:

	def make_frequency_dict(self, text):
		"""Calculate frequency of each character in the text and return as a dict.
		
		This is the first step in Huffman coding. We need to know how often each
		character appears to assign shorter codes to more frequent characters.
		
		Example:
			Input: "AAABBC"
			Output: {'A': 3, 'B': 2, 'C': 1}
		
		Args:
			text: Input text to analyze
			
		Returns:
			Dictionary mapping each character to its frequency count
		"""
		return dict(Counter(text))

	def make_heap(self, frequency):
		"""Make priority queue (min-heap) from frequency dict.
		
		Convert each character and its frequency into a HeapNode and add to the heap.
		The heap automatically maintains min-heap property: node with lowest frequency
		is always at the top. This allows us to efficiently get the two least frequent
		nodes when building the Huffman tree.
		
		Args:
			frequency: Dictionary of character frequencies
		"""
		for key in frequency:
			# Create a leaf node for each character
			node = self.HeapNode(key, frequency[key])
			# Add to min-heap (lowest frequency will be popped first)
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		"""Build Huffman tree by repeatedly merging nodes with lowest frequencies.
		
		This is the core of the Huffman algorithm:
		1. Pop two nodes with lowest frequencies from heap
		2. Create a new internal node with combined frequency
		3. Make the two nodes children of the new node
		4. Push the new node back to heap
		5. Repeat until only one node remains (the root)
		
		Example with frequencies A=3, B=2, C=1:
		- Start: [C(1), B(2), A(3)]
		- Merge C+B: [(CB)(3), A(3)]
		- Merge (CB)+A: [(CBA)(6)] <- Root
		
		After this, heap contains only the root of Huffman tree.
		"""
		while len(self.heap) > 1:
			# Extract two nodes with minimum frequency
			node1 = heapq.heappop(self.heap)  # Lowest frequency
			node2 = heapq.heappop(self.heap)  # Second lowest frequency

			# Create internal node with combined frequency
			# char=None indicates this is not a leaf node
			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1   # Left child (will represent '0' in code)
			merged.right = node2  # Right child (will represent '1' in code)

			# Put merged node back into heap
			heapq.heappush(self.heap, merged) 


	def make_codes_helper(self, root, current_code):
		"""Recursively generate Huffman codes by traversing the tree.
		
		Traverses the Huffman tree depth-first:
		- Going left adds '0' to the code
		- Going right adds '1' to the code
		- When we reach a leaf (node with a character), that's the code for that char
		
		Args:
			root: Current node in tree traversal
			current_code: Binary code accumulated so far (empty string at root)
		"""
		if root is None:
			return

		# If this is a leaf node (has a character), save the code
		if root.char is not None:
			self.codes[root.char] = current_code  # Map character to its code
			self.reverse_mapping[current_code] = root.char  # Map code back to character
			return

		# Recursively traverse left subtree (add '0' to code)
		self.make_codes_helper(root.left, current_code + "0")
		# Recursively traverse right subtree (add '1' to code)
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		"""Generate Huffman codes for all characters in the tree.
		
		Retrieves the root node (only node left in heap after merge_nodes)
		and starts recursive tree traversal to generate codes.
		"""
		# After merge_nodes(), heap has only one element: the root
		root = heapq.heappop(self.heap)
		# Start recursive traversal with empty code string
		self.make_codes_helper(root, "")


	def get_encoded_text(self, text):
		"""Replace each character in text with its Huffman code.
		
		Converts the original text into a binary string using the generated codes.
		
		Example:
			Input text: "AAB"
			Codes: {'A': '0', 'B': '1'}
			Output: "001"
		
		Args:
			text: Original text to encode
			
		Returns:
			Binary string representation of encoded text
		"""
		# Look up each character's code and concatenate them
		return ''.join(self.codes[char] for char in text)


	def pad_encoded_text(self, encoded_text):
		"""Pad encoded text to make its length a multiple of 8 bits (1 byte).
		
		Since we'll store the encoded data as bytes, we need the bit string length
		to be divisible by 8. We add padding zeros and store the padding amount
		in the first 8 bits so we can remove it during decompression.
		
		Example:
			Input: "001" (3 bits)
			Padding needed: 8 - 3 = 5 bits
			Padding info: 00000101 (5 in 8-bit binary)
			Output: "00000101" + "00100000" = "0000010100100000" (16 bits = 2 bytes)
			         ^padinfo^     ^data+pad^
		
		Args:
			encoded_text: Binary string of variable length
			
		Returns:
			Padded binary string with padding info prepended
		"""
		BITS_PER_BYTE = 8
		# Calculate how many bits we need to add
		extra_padding = BITS_PER_BYTE - len(encoded_text) % BITS_PER_BYTE
		# Add padding zeros
		encoded_text += "0" * extra_padding

		# Store padding amount as 8-bit binary at the beginning
		# This allows us to remove exact padding during decompression
		padded_info = f"{extra_padding:08b}"
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		"""Convert binary string into byte array for file storage.
		
		Takes the binary string (e.g., "01001010") and converts each 8-bit
		chunk into an actual byte value (0-255) that can be written to a file.
		
		Example:
			Input: "0100101001100001"  (16 bits)
			Chunk 1: "01001010" = 74 in decimal
			Chunk 2: "01100001" = 97 in decimal
			Output: bytearray([74, 97])
		
		Args:
			padded_encoded_text: Binary string with length multiple of 8
			
		Returns:
			bytearray containing the compressed data
			
		Raises:
			ValueError: If text length is not divisible by 8
		"""
		BITS_PER_BYTE = 8
		# Sanity check: length must be multiple of 8
		if len(padded_encoded_text) % BITS_PER_BYTE != 0:
			raise ValueError("Encoded text not padded properly")

		b = bytearray()
		# Process 8 bits at a time
		for i in range(0, len(padded_encoded_text), BITS_PER_BYTE):
			# Extract 8-bit chunk
			byte = padded_encoded_text[i:i + BITS_PER_BYTE]
			# Convert binary string to integer (base 2) and add to byte array
			b.append(int(byte, 2))
		return b


	def compress(self):
		"""Main compression method that orchestrates the entire Huffman encoding process.
		
		Compression pipeline:
		1. Read input file
		2. Calculate character frequencies
		3. Build Huffman tree
		4. Generate Huffman codes
		5. Encode text using codes
		6. Pad to byte boundary
		7. Convert to bytes and write to file
		
		Returns:
			Path to the compressed output file (.bin)
		"""
		# Create output filename by replacing extension with .bin
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"

		with open(self.path, 'r') as file, open(output_path, 'wb') as output:
			# Read input text and remove trailing whitespace
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


