R = 256  # ASCII characters
Q = 997  # Modulus


def get_hash(key, length):
    """
    Computes the hash value for a given key using the specified length.

    Args:
        key (str): The string for which the hash value is computed.
        length (int): The length of the substring to hash.

    Returns:
        int: The hash value of the substring.
    """
    h = 0
    for j in range(length):
        h = (R * h + ord(key[j])) % Q
    return h


def search(txt_file, pattern):
    """
    Searches for a pattern in a text file using the Rabin-Karp algorithm.

    Args:
        txt_file (str): The path to the text file to search.
        pattern (str): The pattern to search for.

    Returns:
        None
    """
    length_pattern = len(pattern)
    hash_pattern = get_hash(pattern, len(pattern))

    # Precompute R^(M–1) mod(Q)
    RM = 1
    for _ in range(length_pattern - 1):
        RM = (R * RM) % Q

    with open(txt_file, 'r') as file:
        content = file.read()
        length_content = len(content)
        txt_hash = get_hash(content, len(pattern))

        # Check the hash of the first window
        if txt_hash == hash_pattern:
            print("Pattern found at index:", 0)
        
        # Slide the pattern over text
        for i in range(length_pattern, length_content):
            # Remove the influence of the outgoing character (the character at i - M)
            txt_hash = (txt_hash + Q - RM * ord(content[i - length_pattern]) % Q) % Q

            # Add the influence of the incoming character (the character at i)
            txt_hash = (txt_hash * R + ord(content[i])) % Q

            if txt_hash == hash_pattern:
                print("Pattern found at index:", i - length_pattern + 1)


def main():
    pattern = "pattern"
    file = "data/text.txt"
    search(file, pattern)


if __name__ == "__main__":
    main()