def boyer_moore(pattern):
    """
    Preprocesses the pattern to create the 'right' array for the Boyer-Moore algorithm.
    
    Args:
        pattern (str): The pattern to be searched.
    
    Returns:
        list: An array indicating the last occurrence of each character in the pattern.
    """
    R = 256  # ASCII characters
    right = [-1] * R

    # Populate the 'right' array with the last occurrence of each character in the pattern
    for j, char in enumerate(pattern):
        right[ord(char)] = j

    return right


def search(txt_file, pattern):
    """
    Searches for the pattern in the given text file using the Boyer-Moore algorithm and prints the starting indices of matches.
    
    Args:
        txt_file (str): The path to the text file to search.
        pattern (str): The pattern to search for.
    """
    length_pattern = len(pattern)
    right = boyer_moore(pattern)  # Preprocess the pattern

    with open(txt_file, 'r') as file:
        content = file.read()
        length_content = len(content)

        i = 0

        # Iterate over the text content
        while i <= length_content - length_pattern:
            skip = 0

            # Compare the pattern with the text from right to left
            for j in range(length_pattern - 1, -1, -1):
                if pattern[j] != content[i + j]:
                    # Calculate the skip value based on the mismatch
                    skip = max(1, j - right[ord(content[i + j])])
                    break

            # If no mismatch, pattern is found
            if skip == 0:
                print("Pattern found at index:", i)  # Print the starting index of the match
                i += length_pattern  # Move to the next position after the pattern

            i += skip  # Move to the next position based on the skip value


def main():
    """
    The main function to execute the search on a given text file with a specified pattern.
    """
    pattern = "pattern"
    file = "data/text.txt"
    search(file, pattern)


if __name__ == "__main__":
    main()
