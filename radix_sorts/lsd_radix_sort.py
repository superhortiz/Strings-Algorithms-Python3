# Extended ASCII
RADIX = 256


def lsd_sort(string_array, width):
    """
    Performs LSD (Least Significant Digit) radix sort on an array of strings.
    
    Args:
        string_array (list): The list of strings to be sorted.
        width (int): Fixed length of the strings in the array.
    """
    n = len(string_array)
    aux = [''] * n

    for index in range(width - 1, -1, -1):
        count = [0] * (RADIX + 1)

        # Count frequencies of each letter using key as index
        for string in string_array:
            count[ord(string[index]) + 1] += 1

        # Compute frequency cumulates which specify destinations
        for i in range(RADIX):
            count[i + 1] += count[i]

        # Access cumulates using key as index to move items
        for string in string_array:
            aux[count[ord(string[index])]] = string
            count[ord(string[index])] += 1

        # Copy back into original array
        for i in range(n):
            string_array[i] = aux[i]


def main():
    """
    Main function to demonstrate LSD radix sort.
    """
    a = ['dab', 'add', 'cab', 'fad', 'fee', 'bad', 'dad', 'bee', 'fed', 'bed', 'ebb', 'ace']
    print(f"Array before ordering: {a}")
    lsd_sort(a, len(a[0]))
    print(f"Array after ordering:  {a}")


if __name__ == "__main__":
    main()