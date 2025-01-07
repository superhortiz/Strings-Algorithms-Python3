import struct

R = 256
lg_R = 8


def compress(input_file, output_file):
    """
    Compresses an input text file using run-length encoding and writes the compressed data to an output binary file.

    Args:
        input_file (str): The path to the input text file to be compressed.
        output_file (str): The path to the output binary file where the compressed data will be written.

    Returns:
        None
    """
    count = 0
    old = '0'  # Initialize the starting bit to '0'

    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:

        # Read one byte at a time from the input file until the end of the file is reached
        while byte := infile.read(1):

            # Transform to bynary representation
            binary_representation = format(ord(byte), '08b')

            for bit in binary_representation:

                # If the bit changed then write the number of times it appeared
                if bit != old:
                    outfile.write(struct.pack('B', count))

                    # Reset the count
                    count = 0
                    old = bit

                # We have reached the maximum, we intersperse runs of length 0
                elif count == R - 1:
                    outfile.write(struct.pack('B', count))
                    count = 0
                    outfile.write(struct.pack('B', count))

                # Update count
                count += 1

        # Write the last sequence of bits
        outfile.write(struct.pack('B', count))


def expand(input_file, output_file):
    """
    Expands a compressed binary file using run-length decoding and writes the decompressed data to an output text file.

    Args:
        input_file (str): The path to the input binary file to be decompressed.
        output_file (str): The path to the output text file where the decompressed data will be written.

    Returns:
        None
    """
    bit = 0  # Initialize the starting bit to '0'

    with open(input_file, 'rb') as infile, open(output_file, 'w') as outfile:
        # Initialize a buffer to accumulate bits until a full byte is formed and a counter to track the number of bits
        bits = 0
        length_bits = 0

        # Read one byte at a time from the input file until the end of the file is reached
        while run := infile.read(1):

            # Unpack the byte to get the number of consecutive bits to append
            run_length = struct.unpack('B', run)[0]

            # Append the current bit to the list run_length times
            for _ in range(run_length):
                bits = (bits << 1) | bit
                length_bits += 1

                # When we've accumulated enough bits to form a byte (8 bits), write it as an ASCII character
                if length_bits == lg_R:
                    ascii_character = chr(bits)
                    outfile.write(ascii_character)

                    # Reset the buffer and counter to start accumulating the next byte
                    bits = 0
                    length_bits = 0
            
            # Change the value of bit
            bit = 1 if bit == 0 else 0


def main():
    """
    Main function to test the compression and expansion of a sample ASCII file.
    """
    file = 'data/run_length_coding/input.txt'
    compressed_file = 'data/run_length_coding/compressed.bin'
    expanded_file = 'data/run_length_coding/expanded.txt'

    # Create a sample ASCII file for testing
    text = "ABRACADABRA!"
    with open(file, 'w') as f:
        f.write(text)
    print(f"File created with the content: {text}")

    # Compress the file
    compress(file, compressed_file)
    print(f"Compression completed.")

    # Expand the compressed file
    expand(compressed_file, expanded_file)
    print("Expansion completed.")
    with open(expanded_file, 'r') as f:
        print(f"Content expanded: {f.read()}")


if __name__ == "__main__":
    main()