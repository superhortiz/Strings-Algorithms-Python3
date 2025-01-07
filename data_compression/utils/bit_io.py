class BitWriter:
    """
    A class for writing bits to a file. This class buffers bits and writes them to the file in byte format.
    """
    def __init__(self, file):
        """
        Initialize the BitWriter with the given file.
        
        Args:
            file: A file object opened in binary write mode.
        """
        self.file = file
        self.bits = 0           # Buffer to store bits before writing them as a byte
        self.length_bits = 0    # Number of bits currently in the buffer

    def write_bit(self, bit):
        """
        Write a single bit to the buffer. When the buffer is full, write it to the file as a byte.
        
        Args:
            bit: The bit to write (0 or 1).
        """
        self.bits = (self.bits << 1) | int(bit)
        self.length_bits += 1

        # When the buffer is full, write it to the file as a byte
        if self.length_bits == 8:
            self.file.write(bytes([self.bits]))
            self.bits = 0
            self.length_bits = 0

    def write_byte(self, byte):
        """
        Write a byte to the buffer bit by bit.
        
        Args:
            byte: The byte to write.
        """

        # Convert the byte to its binary representation
        binary_representation = format(ord(byte), '08b')

        # Write each bit to the buffer
        for bit in binary_representation:
            self.write_bit(bit)

    def write_bits(self, value, width):
        """
        Write a character to the buffer as a specified number of bits.
        
        Args:
            char: The character to write.
            width: The number of bits to use for the binary representation.
        """

        # Convert the character to its binary representation, padded to the specified width
        binary_representation = format(value, '0' + str(width) + 'b')

        # Write each bit to the buffer
        for bit in binary_representation:
            self.write_bit(bit)

    def close(self):
        """
        Flush any remaining bits in the buffer to the file as a byte. 
        This ensures that all bits are written when closing the file.
        """
        if self.length_bits > 0:

            # Pad the remaining bits to form a complete byte
            self.bits = self.bits << (8 - self.length_bits)
            self.file.write(bytes([self.bits]))


class BitReader:
    """
    A class for reading bits and bytes from a binary string representation of content.
    This class allows for sequential bit and byte reading.
    """
    def __init__(self, content):
        """
        Initialize the BitReader with the given binary content.
        
        Args:
            content: A bytes object containing the binary content.
        """
        # Convert the content to a binary string representation
        self.binary_string = ''.join(format(byte, '08b') for byte in content)
        self.index = 0  # Initialize the index for reading bits

    def read_bit(self):
        """
        Read a single bit from the binary string.
        
        Returns:
            The next bit in the binary string.
        """
        bit = self.binary_string[self.index]  # Get the bit at the current index
        self.index += 1  # Increment the index for the next read
        return bit

    def read_byte(self):
        """
        Read the next byte (8 bits) from the binary string.
        
        Returns:
            The next byte in the binary string.
        """
        byte = self.binary_string[self.index: self.index + 8]  # Get the byte at the current index
        self.index += 8  # Increment the index by the length of a byte
        return byte

    def read_bits(self, width):
        """
        Read the next specified number of bits from the binary string.
        
        Args:
            width: The number of bits to read.
        
        Returns:
            The next 'width' bits in the binary string.
        """
        bits = self.binary_string[self.index: self.index + width]  # Get the bits at the current index
        self.index += width  # Increment the index by the number of bits read
        return bits
