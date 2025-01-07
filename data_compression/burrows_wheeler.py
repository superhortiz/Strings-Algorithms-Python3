from collections import deque
from huffman import Huffman


R = 256  # Extended ASCII


def counting_sort(string):
    """
    Perform a key-index counting sort on the input string and return the sorted indices.

    Args:
        string (str): The input string to be sorted.

    Returns:
        list: A list of indices representing the sorted order of characters in the input string.
    """
    length = len(string)
    indices = [0] * length
    count = [0] * (R + 1)

    # Count frequencies of each character
    for i in range(length):
        count[ord(string[i]) + 1] += 1

    # Compute cumulative counts
    for r in range(R):
        count[r + 1] += count[r]

    # Place the indices of the characters in the sorted order
    for i in range(length):
        indices[count[ord(string[i])]] = i
        count[ord(string[i])] += 1

    return indices

def circular_suffix_array(string):
    """
    Generates the circular suffix array of a given string using a 3-way radix quicksort.
    
    Args:
        string (str): The input string for which to compute the circular suffix array.

    Returns:
        list: A list of starting indices that represent the lexicographically sorted circular suffixes of the input string.
    """
    length = len(string)

    # Initialize the indices list with starting positions of suffixes
    indices = list(range(length))

    def sort(string, lo, hi, depth, length):
        """
        Recursive 3-way radix quicksort to sort the suffixes.
        
        Args:
            string (str): The input string.
            lo (int): The lower bound of the current partition.
            hi (int): The upper bound of the current partition.
            depth (int): The current character depth to consider in sorting.
            length (int): The length of the input string.
        """
        if hi <= lo or depth >= length:
            return

        less_than, greater_than = lo, hi

        # Select the pivot character, considering circular behavior
        pivot = string[(indices[lo] + depth) % length]

        i = lo + 1

        while i <= greater_than:
            t = string[(indices[i] + depth) % length]

            if t < pivot:
                # Swap and move less_than and i pointers
                indices[less_than], indices[i] = indices[i], indices[less_than]
                less_than += 1
                i += 1

            elif t > pivot:
                # Swap and move greater_than pointer
                indices[greater_than], indices[i] = indices[i], indices[greater_than]
                greater_than -= 1

            else:
                # Move i pointer if the characters are equal to the pivot
                i += 1

        # Recursively sort the three partitions
        sort(string, lo, less_than - 1, depth, length)
        sort(string, less_than, greater_than, depth + 1, length)
        sort(string, greater_than + 1, hi, depth, length)

    # Initial call to the sorting function
    sort(string, 0, length - 1, 0, length)

    # Return the sorted indices representing the circular suffix array
    return indices

def burrows_wheeler_transform(string):
    """
    Perform the Burrows-Wheeler Transform on the given input string.

    Args:
        string (str): The input string to be transformed.

    Returns:
        tuple: A tuple containing the index of the original string in the sorted suffix array and the transformed string.
    """
    length = len(string)

    # Get the starting indices of the sorted circular suffixes of the input
    indices = circular_suffix_array(string)
    transform = [""] * length

    # Build the transformed string
    for i, index in enumerate(indices):
        transform[i] = string[(index + length - 1) % length]

        # Track the position of the original string in the sorted suffix array
        if index == 0:
            first = i

    return first, ''.join(transform)

def burrows_wheeler_inverse(first, transform):
    """
    Perform the Burrows-Wheeler Inverse Transform on the given input.

    Args:
        first (int): The index of the original string in the sorted suffix array.
        transform (str): The transformed string.

    Returns:
        str: The original string before the Burrows-Wheeler Transform.
    """
    # Get the sorted order of characters and their next indices
    next_list = counting_sort(transform)
    next_index = first
    inverse = []

    # Reconstruct the original string
    for i in range(len(transform)):
        inverse.append(transform[next_list[next_index]])
        next_index = next_list[next_index]

    return ''.join(inverse)

def move_to_front_encode(string):
    """
    Perform move-to-front encoding on the input string.

    Args:
        string (str): The input string to be encoded.

    Returns:
        list: A list of integers representing the move-to-front encoded values.
    """

    # Initialize the symbol table as a deque containing ASCII characters
    symbol_table = deque([chr(i) for i in range(R)])
    encoded = []  # List to store the encoded output
    
    for char in string:
        # Find the index of the current character in the symbol table
        index = symbol_table.index(char)
        
        # Append the index to the encoded output
        encoded.append(index)
        
        # Move the character to the front of the symbol table
        symbol_table.remove(char)
        symbol_table.appendleft(char)

    return encoded

def move_to_front_decode(encoded):
    """
    Perform move-to-front decoding on the encoded list.

    Args:
        encoded (list): A list of integers representing the move-to-front encoded values.

    Returns:
        str: The original string after decoding.
    """

    # Initialize the symbol table as a deque containing ASCII characters
    symbol_table = deque([chr(i) for i in range(R)])

    # List to store the decoded characters
    decoded = []

    for code in encoded:
        # Get the character from the symbol table using the index
        char = symbol_table[code]

        # Append the character to the decoded output
        decoded.append(char)

        # Move the character to the front of the symbol table
        symbol_table.remove(char)
        symbol_table.appendleft(char)

    return ''.join(decoded)

def compress(input_file, compressed_file, trie_file):
    """
    Compress the content of an input file using Burrows-Wheeler transform, 
    Move-to-Front encoding, and Huffman coding. The compressed data is written
    to the compressed file, and the Huffman trie is written to the trie file.

    Args:
        input_file (str): The path to the input file containing the original content.
        compressed_file (str): The path to the file where the compressed data will be written.
        trie_file (str): The path to the file where the Huffman trie will be written.
    """
    # Read the content from the input file
    with open(input_file, 'r') as file:
        content = file.read()

        # Apply the Burrows-Wheeler transform
        first, transformed = burrows_wheeler_transform(content)

        # Apply Move-to-Front encoding to the transformed string
        encoded = move_to_front_encode(transformed)

        # Convert the 'first' index to a 32-bit binary string and append its bytes to the encoded data
        binary_first = format(first, '032b')
        n_bytes = 4  # Number of bytes in the 32-bit binary string
        n_bits = 8  # Number of bits in a byte

        for i in range(n_bytes):
            binary = binary_first[i*n_bits:i*n_bits+n_bits]
            encoded.append(int(binary, 2))

        # Create a Huffman encoder instance and compress the encoded data
        huffman = Huffman()
        huffman.compress_indices(encoded, compressed_file, trie_file)

def expand(compressed_file, expanded_file, trie_file):
    """
    Decompress the content of a compressed file using Huffman decoding, 
    Move-to-Front decoding, and Burrows-Wheeler inverse transform. 
    The decompressed data is written to the expanded file.

    Args:
        compressed_file (str): The path to the file containing compressed data.
        expanded_file (str): The path to the file where the decompressed data will be written.
        trie_file (str): The path to the file containing the Huffman trie.
    """
    # Create a Huffman decoder instance and expand the compressed data to get encoded indices
    huffman = Huffman()
    decoded = huffman.expand_indices(compressed_file, trie_file)

    # Initialize variables to store the first index
    n_bytes = 4  # Number of bytes in the 32-bit integer
    n_bits = 8   # Number of bits in a byte
    binary_first = ""

    # Retrieve and remove the 'first' index from the decoded data
    # The 'first' index is stored as the last 4 bytes of the decoded data
    for i in range(n_bytes):
        first = decoded.pop()
        binary = format(first, '08b')  # Convert the byte to an 8-bit binary string
        binary_first = binary + binary_first  # Concatenate to build the 32-bit binary string

    # Convert the 32-bit binary string to an integer
    first = int(binary_first, 2)

    # Apply Move-to-Front decoding to the remaining data
    transformed = move_to_front_decode(decoded)

    # Apply Burrows-Wheeler inverse transform to reconstruct the original content
    decoded_content = burrows_wheeler_inverse(first, transformed)
    
    # Write the decoded content to the expanded file
    with open(expanded_file, 'w') as file:
        file.write(decoded_content)

def main():
    """
    Main function to demonstrate Burrows-Wheeler compression and decompression.
    """
    # Define file paths
    input_file = 'data/burrows_wheeler/input.txt'
    compressed_file = 'data/burrows_wheeler/compressed.bin'
    trie_file = 'data/burrows_wheeler/trie_file.bin'
    expanded_file = 'data/burrows_wheeler/expanded.txt'

    # Perform Burrows-Wheeler compression
    compress(input_file, compressed_file, trie_file)
    print(f"Compression completed.")

    # Perform Burrows-Wheeler decompression
    expand(compressed_file, expanded_file, trie_file)
    print("Expansion completed.")


if __name__ == "__main__":
    main()
