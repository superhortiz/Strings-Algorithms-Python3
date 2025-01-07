def longest_common_prefix(string_a, string_b):
    """
    Computes the length of the longest common prefix between two strings.
    
    Args:
        string_a (str): The first string.
        string_b (str): The second string.
    
    Returns:
        int: The length of the longest common prefix.
    """
    n = min(len(string_a), len(string_b))

    for i in range(n):
        if string_a[i] != string_b[i]:
            return i

    return n


def longest_repeated_substring(string):
    """
    Finds the longest repeated substring in a given string.
    
    Args:
        string (str): The input string.
    
    Returns:
        str: The longest repeated substring.
    """
    n = len(string)
    suffixes = []

    for i in range(n):
        suffixes.append(string[i:])

    suffixes.sort()
    lrs = ""

    for i in range(n - 1):
        length = longest_common_prefix(suffixes[i], suffixes[i + 1])

        if length > len(lrs):
            lrs = suffixes[i][0:length]

    return lrs


def main():
    """
    Main function to demonstrate finding the longest repeated substring.
    """
    string = "banana"
    print(f"Longest repeated substring for string \"{string}\": \"{longest_repeated_substring(string)}\"")


if __name__ == "__main__":
    main()