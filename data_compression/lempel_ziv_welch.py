from utils.tst import TST
from utils.bit_io import BitWriter, BitReader


R = 256  # ASCII characters
CODE_WIDTH = 12  # Codeword width
NUM_CODES = 4096  # Number of codewords 2^12


def compress(input_file, compressed_file):
    """
    Compresses the input file using the LZW (Lempel-Ziv-Welch)
    algorithm and writes the compressed data to the output file.
    
    Args:
        input_file: Path to the input file to be compressed.
        compressed_file: Path to the output file where compressed data will be written.
    """
    # Create a Ternary Search Trie to use as a symbol table.
    # During compression, we need to repeatedly look for the longest prefix that matches the current input.
    # A Ternary Search Trie (TST) is efficient for this purpose because it provides fast lookups, insertions, and deletions.
    symbol_table = TST()
    for i in range(R):
        # Codewords for singlechars, radix R keys
        symbol_table.put(chr(i), i)

    # We start the new coding from R + 1.
    # The value R is reserved for the end-of-file (EOF) codeword.
    code = R + 1
    EOF = R

    with open(input_file, 'r') as infile, open(compressed_file, 'wb') as outfile:
        # Read all the content of the input file
        content = infile.read()

        # Initialize a BitWriter object to handle bit-level writing
        writer = BitWriter(outfile)

        while len(content) > 0:
            # Find longest prefix match
            longest_prefix = symbol_table.longest_prefix_of(content)

            # Write W-bit codeword for longest_prefix
            writer.write_bits(symbol_table.get(longest_prefix), CODE_WIDTH)

            len_prefix = len(longest_prefix)

            if len_prefix < len(content) and code < NUM_CODES:

                # Add new codeword to the trie, including the next character in the input
                symbol_table.put(content[0:len_prefix + 1], code)
                code += 1

            # Crop the input until the characters we haven't encoded
            content = content[len_prefix:]

        # Write stop codeword and close input stream
        writer.write_bits(EOF, CODE_WIDTH)
        writer.close()

def expand(compressed_file, output_file):
    """
    Expands a compressed file using the LZW (Lempel-Ziv-Welch) algorithm 
    and writes the decompressed data to the output file.

    Args:
        compressed_file: Path to the compressed input file.
        output_file: Path to the output file where decompressed data will be written.
    """

    # Create a list to use as a symbol table.
    # Now we work with a predefined and static set of codewords that map to strings.
    # A list allows for efficient access by index.
    symbol_table = [""] * NUM_CODES

    # Initialize table for single-character codewords.
    # Each index represents an ASCII character.
    for i in range(R):
        symbol_table[i] = chr(i)

    # We start the new coding from R + 1.
    # The value R is reserved for the end-of-file (EOF) codeword.
    next_code = R + 1
    EOF = R

    with open(compressed_file, 'rb') as infile, open(output_file, 'w') as outfile:
        # Initialize a BitReader object to handle bit-level reading from the compressed file
        reader = BitReader(infile.read())

        # Read the first codeword from the input.
        # Use the codeword to get the corresponding string from the symbol table.
        codeword = int(reader.read_bits(CODE_WIDTH), 2)
        value = symbol_table[codeword]

        while True:
            # Write the current substring to the output file.
            outfile.write(value)

            # Read the next codeword from the input file.
            codeword = int(reader.read_bits(CODE_WIDTH), 2)

            # If the codeword is the EOF marker, break the loop.
            if codeword == EOF:
                break

            # Retrieve the string corresponding to the new codeword
            current_string = symbol_table[codeword]

            # This part deals with the tricky case. If the new codeword
            # equals the codeword we have not read yet
            if next_code == codeword:
                # Construct the new string from the current string by adding its first character
                current_string = value + value[0]

            # If there is still room in the symbol table
            if next_code < NUM_CODES:
                # Add new entry to the symbol table.
                symbol_table[next_code] = value + current_string[0]
                next_code += 1

            # Update the value for the next iteration
            value = current_string


def main():
    """
    Main function to demonstrate LZW compression and decompression.
    """
    # Define file paths
    input_file = 'data/lempel_ziv_welch/input.txt'
    compressed_file = 'data/lempel_ziv_welch/compressed.bin'
    expanded_file = 'data/lempel_ziv_welch/expanded.txt'

    # Perform LZW compression
    compress(input_file, compressed_file)
    print(f"Compression completed.")

    # Perform LZW decompression
    expand(compressed_file, expanded_file)
    print("Expansion completed.")


if __name__ == "__main__":
    main()