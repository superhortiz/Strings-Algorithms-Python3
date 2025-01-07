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


def sort(string_array, lo, hi, depth):
    """
    Sorts the array of strings using three-way radix quicksort.
    
    Args:
        string_array (list): The list of strings to be sorted.
        lo (int): The lower index of the array to sort.
        hi (int): The higher index of the array to sort.
        depth (int): The current depth of the character being sorted.
    """
    if hi <= lo:
        return

    # Initialize pointers for less than and greater than partitions
    less_than, greater_than = lo, hi

    # Choose the partitioning element (pivot)
    pivot = char_at(string_array[lo], depth)

    # Initialize the current element pointer
    i = lo

    while i <= greater_than:
        t = char_at(string_array[i], depth)
        if t < pivot:
            # Element is less than pivot, swap with element at less_than and move both pointers
            string_array[less_than], string_array[i] = string_array[i], string_array[less_than]
            i += 1
            less_than += 1

        elif t > pivot:
            # Element is greater than pivot, swap with element at greater_than and move greater_than pointer
            string_array[i], string_array[greater_than] = string_array[greater_than], string_array[i]
            greater_than -= 1

        else:
            # Element is equal to pivot, just move the current element pointer
            i += 1

    # Recursively sort the subarrays
    sort(string_array, lo, less_than - 1, depth)

    if pivot != '\0':
        sort(string_array, less_than, greater_than, depth + 1)
    
    sort(string_array, less_than + 1, hi, depth)


def quick_sort(string_array):
    """
    Performs three-way radix quicksort on an array of strings.
    
    Args:
        string_array (list): The list of strings to be sorted.
    """
    n = len(string_array)
    sort(string_array, 0, n - 1, 0)


def main():
    """
    Main function to demonstrate three-way radix quicksort.
    """
    a = ['she', 'sells', 'seashells', 'by', 'the', 'sea', 'shore', 'the', 'shells', 'she', 'sells', 'are', 'surely', 'seashells']
    print(f"Array before ordering: {a}")
    quick_sort(a)
    print(f"Array after ordering:  {a}")


if __name__ == "__main__":
    main()