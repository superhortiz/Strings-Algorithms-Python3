def KMP(pattern):
    """
    Builds the deterministic finite automaton (DFA) for a given pattern.

    Args:
        pattern (str): The pattern to search for.

    Returns:
        list: A 2D list representing the DFA.
    """
    R = 256  # ASCII characters
    pattern_length = len(pattern)
    dfa = [[0] * pattern_length for _ in range(R)]

    # Define dfa for state = 0:
    # Assign 1 for matching the first character in the pattern.
    # Assign 0 for the other characters.
    restart_state = 0
    dfa[ord(pattern[0])][restart_state] = 1

    # Iterate over the pattern
    for j in range(1, pattern_length):

        # Iterate over all the possible characters
        for char in range(R):

            # Copy mismatch cases from restart state
            dfa[char][j] = dfa[char][restart_state]

        # Set match case
        dfa[ord(pattern[j])][j] = j + 1

        # Update restart state. This will depend on the pattern
        restart_state = dfa[ord(pattern[j])][restart_state]

    return dfa


def search(txt_file, pattern):
    """
    Searches for a pattern in a text file and prints the positions of matches.

    Args:
        txt_file (str): The path to the text file to search.
        pattern (str): The pattern to search for.
    """
    length_pattern = len(pattern)
    dfa = KMP(pattern)

    with open(txt_file, 'r') as file:
        content = file.read()
        length_content = len(content)
        state = 0

        for index, char in enumerate(content):
            state = dfa[ord(char)][state]

            if state == length_pattern:
                print("Pattern found at index:", index - length_pattern + 1)
                state = 0


def main():
    """The main function that defines the pattern and the file to search in."""
    pattern = "pattern"
    file = "data/text.txt"
    search(file, pattern)


if __name__ == "__main__":
    main()