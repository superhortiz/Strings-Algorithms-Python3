import struct
import heapq
from utils.bit_io import BitWriter, BitReader


class Huffman:
    """
    Huffman coding for data compression and decompression.
    """
    R = 256  # ASCII characters

    class Node:
        """
        A node in the Huffman tree.
        """

        def __init__(self, char, frequency, left=None, right=None):
            """
            Initialize a Huffman tree node.

            Args:
                char: The character stored in the node.
                frequency: The frequency of the character.
                left: The left child node.
                right: The right child node.
            """
            self.char = char
            self.frequency = frequency
            self.left = left
            self.right = right

        def is_leaf(self):
            """
            Check if the node is a leaf node.

            Returns:
                bool: True if the node is a leaf node, False otherwise.
            """
            return self.left is None and self.right is None

        def __lt__(self, other):
            """
            Less-than comparison based on frequency, for use in priority queue.

            Args:
                other: Another Huffman.Node to compare with.

            Returns:
                bool: True if this node's frequency is less than the other node's frequency.
            """
            return self.frequency < other.frequency

    def __init__(self):
        """
        Initialize the Huffman encoder/decoder.
        """
        self.root = None
        self.bit_reader = None
        self.bit_writer = None

    def expand(self, compressed_file, expanded_file, trie_file):
        """
        Decompress a file using the Huffman coding trie.

        Args:
            compressed_file: The file containing the compressed data.
            expanded_file: The output file for the decompressed data.
            trie_file: The file containing the encoded trie.
        """
        # Decode the encoded trie from the file and set the root node
        self.root = self.read_trie(trie_file)

        # Open the input file in binary read mode and the output file in write mode
        with open(compressed_file, 'rb') as infile, open(expanded_file, 'w') as outfile:

            # Read the number of characters that are encoded in 16 bits
            total_chars = struct.unpack('H', infile.read(2))[0]

            # Initialize the counter for the number of characters written to the output file
            char_written = 0

            # Initialize traversal from the root node of the trie
            node = self.root

            # Read bytes from the input file
            while byte := infile.read(1):

                # Convert the byte to its binary representation (8 bits)
                binary_representation = format(ord(byte), '08b')

                # Iterate over each bit in the binary representation
                for bit in binary_representation:

                    # Traverse to the left child node if the bit is '0'
                    if bit == '0':
                        node = node.left

                    # Traverse to the right child node if the bit is '1'
                    else:
                        node = node.right

                    # If the current node is a leaf, write the character to the output file
                    # and reset the traversal to the root node
                    if node.is_leaf():
                        outfile.write(node.char)
                        node = self.root

                        # Check if the total number of characters has been written
                        char_written += 1
                        if char_written == total_chars:
                            break

    def expand_indices(self, compressed_file, trie_file):
        """
        Decompress a file using the Huffman coding trie and retrieve the indices.
        This method is specially adapted to handle the expansion for Burrows-Wheeler transform,
        where the output is a list of indices.

        Args:
            compressed_file: The file containing the compressed data.
            trie_file: The file containing the encoded trie.
        """
        # Decode the encoded trie from the file and set the root node
        self.root = self.read_trie(trie_file)
        indices = []

        # Open the input file in binary read mode and the output file in write mode
        with open(compressed_file, 'rb') as infile:

            # Read the number of characters that are encoded in 16 bits
            total_chars = struct.unpack('H', infile.read(2))[0]

            # Initialize the counter for the number of characters written to the output file
            char_written = 0

            # Initialize traversal from the root node of the trie
            node = self.root

            # Read bytes from the input file
            while byte := infile.read(1):

                # Convert the byte to its binary representation (8 bits)
                binary_representation = format(ord(byte), '08b')

                # Iterate over each bit in the binary representation
                for bit in binary_representation:

                    # Traverse to the left child node if the bit is '0'
                    if bit == '0':
                        node = node.left

                    # Traverse to the right child node if the bit is '1'
                    else:
                        node = node.right

                    # If the current node is a leaf, write the character to the output file
                    # and reset the traversal to the root node
                    if node.is_leaf():
                        indices.append(ord(node.char))
                        node = self.root

                        # Check if the total number of characters has been written
                        char_written += 1
                        if char_written == total_chars:
                            break
        return indices

    def write_trie(self, trie_file):
        """
        Write the Huffman trie to a file.

        Args:
            trie_file: The file to write the trie to.
        """
        # Open the specified file in binary write mode
        with open(trie_file, 'wb') as file:

            # Initialize a BitWriter object to handle bit-level writing
            self.bit_writer = BitWriter(file)

            # Write the trie structure starting from the root node
            self._write_trie(self.root)

            # Close the BitWriter to ensure all bits are properly written
            self.bit_writer.close()

    def _write_trie(self, node):
        """
        Recursively write the Huffman trie to a BitWriter.

        Args:
            node: The current node in the Huffman tree.
        """
        # If the current node is a leaf, write a '1' to indicate a leaf node
        # Then write the binary representation of the character stored in the node
        if node.is_leaf():
            self.bit_writer.write_bit(1)
            self.bit_writer.write_byte(node.char)
            return

        # If the current node is an internal node, write a '0' to indicate it's not a leaf
        self.bit_writer.write_bit(0)

        # Recursively write the left and right child nodes
        self._write_trie(node.left)
        self._write_trie(node.right)

    def read_trie(self, trie_file):
        """
        Read the Huffman trie from a file.

        Args:
            trie_file: The file containing the encoded trie.

        Returns:
            Huffman.Node: The root node of the Huffman tree.
        """
        # Open the specified file in binary read mode
        with open(trie_file, 'rb') as file:

            # Initialize a BitReader object to read the binary content of the file
            self.bit_reader = BitReader(file.read())

            # Read and return the root node of the trie
            return self._read_trie()

    def _read_trie(self):
        """
        Recursively read the Huffman trie from a BitReader.

        Returns:
            Huffman.Node: The current node in the Huffman tree.
        """
        # If the next bit is '1', it's a leaf node
        if self.bit_reader.read_bit() == '1':

            # Read the 8 bits corresponding to the character's ASCII value
            # Convert the binary string to an ASCII value and then to a character
            # Create a leaf node with the character, frequency = 0, and no children
            ascii_value = int(self.bit_reader.read_byte(), 2)
            char = chr(ascii_value)
            return Huffman.Node(char, 0)

        # If the next bit is '0', it's an internal node. Recursively read the left and right nodes
        node_left = self._read_trie()
        node_right = self._read_trie()

        # Create an internal node with no character value, frequency = 0,
        # and the corresponding left and right children
        return Huffman.Node(None, 0, node_left, node_right)

    def build_trie(self, frequencies):
        """
        Build the Huffman trie based on character frequencies.

        Args:
            frequencies: A list of frequencies for each character.

        Returns:
            Huffman.Node: The root node of the Huffman tree.
        """
        # Initialize a priority queue with singleton tries for each character with a non-zero frequency
        priority_queue = []
        for i in range(Huffman.R):
            if frequencies[i] > 0:
                heapq.heappush(priority_queue, Huffman.Node(chr(i), frequencies[i]))

        # Repeat the process until there is only one trie left in the priority queue
        while len(priority_queue) > 1:

            # Remove the two nodes with the smallest frequencies
            node_x = heapq.heappop(priority_queue)
            node_y = heapq.heappop(priority_queue)

            # Merge two smallest tries with a internal node as parent
            parent = Huffman.Node(None, node_x.frequency + node_y.frequency, node_x, node_y)

            # Put the new trie in the priority queue
            heapq.heappush(priority_queue, parent)

        # Return the root of the trie
        return heapq.heappop(priority_queue)

    def compress(self, input_file, compressed_file, trie_file):
        """
        Compress a file using Huffman encoding and write it to the compressed file.
        The Huffman trie is also written to the trie file for use by the decoder.

        Args:
            input_file: The file containing the original data to be compressed.
            compressed_file: The output file for the compressed data.
            trie_file: The file to write the encoded trie to.
        """
        with open(input_file, 'r') as infile, open(compressed_file, 'wb') as outfile:
            # Read the entire input file content
            content = infile.read()

            # Tabulate frequency counts for each character in the input content
            frequencies = [0] * Huffman.R
            for char in content:
                frequencies[ord(char)] += 1

            # Build the Huffman coding trie based on frequency counts
            self.root = self.build_trie(frequencies)

            # Write the Huffman trie to the trie_file for use by the decoder
            self.write_trie(trie_file)

            # Build the symbol table for encoding using the Huffman trie
            symbol_table = self.build_code()

            # Open a BitWriter instance and write the number of characters in the content
            writer = BitWriter(outfile)
            number_chars = len(content)
            outfile.write(struct.pack('H', number_chars))
            
            # Encode the input content using the Huffman code and write to the compressed file
            for char in content:
                code = symbol_table[ord(char)]

                for bit in code:
                    writer.write_bit(bit)

            # Close the BitWriter to ensure all remaining bits are written to the file
            writer.close()

    def compress_indices(self, content, compressed_file, trie_file):
        """
        Compress the given content using Huffman encoding and write it to the compressed file.
        The Huffman trie is also written to the trie file for use by the decoder.
        This is specially adapted to work with indices for Burrows-Wheeler.

        Args:
            content (list): The input data to be compressed.
            compressed_file (str): The path to the file where the compressed data will be written.
            trie_file (str): The path to the file where the Huffman trie will be written.
        """
        with open(compressed_file, 'wb') as outfile:

            # Tabulate frequency counts for each value in the input content
            frequencies = [0] * Huffman.R
            for value in content:
                frequencies[value] += 1

            # Build the Huffman coding trie based on frequency counts
            self.root = self.build_trie(frequencies)

            # Write the Huffman trie to the trie_file for use by the decoder
            self.write_trie(trie_file)

            # Build the symbol table for encoding using the Huffman trie
            symbol_table = self.build_code()

            # Open a BitWriter instance and write the number of characters in the content
            writer = BitWriter(outfile)
            number_chars = len(content)
            outfile.write(struct.pack('H', number_chars))
            
            # Encode the input content using the Huffman code and write to the compressed file
            for value in content:
                code = symbol_table[value]

                for bit in code:
                    writer.write_bit(bit)

            # Close the BitWriter to ensure all remaining bits are written to the file
            writer.close()

    def build_code(self):
        """
        Builds the symbol table for Huffman encoding. Each character gets its corresponding binary code.

        Returns:
            symbol_table: A list of binary codes for each character.
        """
        symbol_table = [''] * Huffman.R
        self._build_code(symbol_table, self.root, "")
        return symbol_table

    def _build_code(self, symbol_table, node, code):
        """
        Recursively builds the Huffman encoding for each character by traversing the Huffman tree.

        Args:
            symbol_table: The table to store binary codes for characters.
            node: The current node in the Huffman tree.
            code: The binary code generated for the current traversal path.
        """
        # If the node is a leaf, assign the generated code to the corresponding character in the symbol table
        if node.is_leaf():
            symbol_table[ord(node.char)] = code
            return

        # Traverse left and add '0' to the code
        self._build_code(symbol_table, node.left, code + '0')

        # Traverse right and add '1' to the code
        self._build_code(symbol_table, node.right, code + '1')


def main():
    """
    Main function to demonstrate Huffman compression and decompression.
    """
    # Define file paths
    input_file = 'data/huffman/input.txt'
    trie_file = 'data/huffman/trie_file.bin'
    compressed_file = 'data/huffman/compressed.bin'
    expanded_file = 'data/huffman/expanded.txt'

    # Create a Huffman object
    huffman = Huffman()

    # Perform Huffman compression
    huffman.compress(input_file, compressed_file, trie_file)
    print(f"Compression completed.")

    # Perform Huffman decompression
    huffman.expand(compressed_file, expanded_file, trie_file)
    print("Expansion completed.")


if __name__ == "__main__":
    main()