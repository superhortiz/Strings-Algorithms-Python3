# Extended ASCII
RADIX = 256


def char_at(string, position):
    """
    Returns the character at the specified position in the string,
    or '\0' if the position is out of bounds.
    
    Args:
        string (str): The string to get the character from.
        position (int): The position of the character in the string.
    
    Returns:
        str: The character at the specified position or '\0' if out of bounds.
    """
    if position < len(string):
        return string[position]
    return '\0'


def sort(string_array, aux, lo, hi, depth):
    """
    Sorts the array of strings using MSD (Most Significant Digit) radix sort.
    
    Args:
        string_array (list): The list of strings to be sorted.
        aux (list): Auxiliary list for sorting.
        lo (int): The lower index of the array to sort.
        hi (int): The higher index of the array to sort.
        depth (int): The current depth of the character being sorted.
    """

    # Initialize flag to detect if we have reached the end of all strings at the current depth
    end_reached = True

    if hi <= lo:
        return

    count = [0] * (RADIX + 2)

    # Count frequencies of each letter using key as index
    for i in range(lo, hi + 1):
        count[ord(char_at(string_array[i], depth)) + 2] += 1

        if end_reached and char_at(string_array[i], depth) != '\0':
            end_reached = False

    # If all characters are null characters, terminate recursion
    if end_reached:
        return

    # Compute frequency cumulates which specify destinations
    for i in range(RADIX):
        count[i + 1] += count[i]

    # Access cumulates using key as index to move items
    for i in range(lo, hi + 1):
        aux[count[ord(char_at(string_array[i], depth)) + 1]] = string_array[i]
        count[ord(char_at(string_array[i], depth)) + 1] += 1

    # Copy back into original array
    for i in range(lo, hi + 1):
        string_array[i] = aux[i - lo]

    # Sort R subarrays recursively (one per character in R)
    for r in range(RADIX):
        sort(string_array, aux, lo + count[r], lo + count[r + 1] - 1, depth + 1)


def msd_sort(string_array):
    """
    Performs MSD (Most Significant Digit) radix sort on an array of strings.
    
    Args:
        string_array (list): The list of strings to be sorted.
    """
    n = len(string_array)
    aux = [''] * n
    sort(string_array, aux, 0, n - 1, 0)


def main():
    """
    Main function to demonstrate MSD radix sort.
    """
    a = ['she', 'sells', 'seashells', 'by', 'the', 'sea', 'shore', 'the', 'shells', 'she', 'sells', 'are', 'surely', 'seashells']
    print(f"Array before ordering: {a}")
    msd_sort(a)
    print(f"Array after ordering:  {a}")


if __name__ == "__main__":
    main()