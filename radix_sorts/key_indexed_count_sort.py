# Extended ASCII
RADIX = 256


def key_indexed_count_sort(char_array):
    """
    Performs key-indexed counting to sort an array of characters.
    
    Args:
        char_array (list): The list of characters to be sorted.
    """
    n = len(char_array)
    count = [0] * (RADIX + 1)
    aux = [''] * n

    # Count frequencies of each letter using key as index
    for char in char_array:
        count[ord(char) + 1] += 1

    # Compute frequency cumulates which specify destinations
    for i in range(RADIX):
        count[i + 1] += count[i]

    # Access cumulates using key as index to move items
    for char in char_array:
        aux[count[ord(char)]] = char
        count[ord(char)] += 1

    # Copy back into original array
    for i in range(n):
        char_array[i] = aux[i]


def main():
    """
    Main function to demonstrate key-indexed counting.
    """
    a = ['d', 'a', 'c', 'f', 'f', 'b', 'd', 'b', 'f', 'b', 'e', 'a']
    print(f"Array before ordering: {a}")
    key_indexed_count_sort(a)
    print(f"Array after ordering:  {a}")


if __name__ == "__main__":
    main()