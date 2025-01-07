class TST:
    """
    A Ternary Search Trie (TST) data structure.

    The TST supports insertion, searching, and prefix-based retrieval of keys.
    Each node in the TST can have up to three children: left, middle, and right.
    """

    class Node:
        """
        A node in the Ternary Search Trie (TST).

        Each node contains a character, an optional value, and references to
        its left, middle, and right children.
        """
        def __init__(self):
            """Initializes a node in the TST with default values."""
            self.value = None
            self.char = None
            self.left = None
            self.mid = None
            self.right = None

    def __init__(self):
        """Initializes an empty TST."""
        self.root = None
        self.size = 0

    def put(self, key, value):
        """
        Inserts a key-value pair into the TST.

        Args:
            key (str): The key to insert.
            value (any): The value to associate with the key.
        """
        if not self.contains(key):
            self.size += 1
        self.root = self._put(self.root, key, value, 0)

    def _put(self, node, key, value, depth):
        """
        Recursive helper method to insert a key-value pair into the TST.

        Args:
            node (TST.Node): The current node in the TST.
            key (str): The key to insert.
            value (any): The value to associate with the key.
            depth (int): The current depth in the TST.

        Returns:
            TST.Node: The updated node in the TST.
        """
        char = key[depth]

        # Base case: If the node is None, create a new node with the current character
        if node is None:
            node = TST.Node()
            node.char = char

        # Recursive Exploration:
        # Left branch
        if char < node.char:
            node.left = self._put(node.left, key, value, depth)

        # Right branch
        elif char > node.char:
            node.right = self._put(node.right, key, value, depth)

        # Middle branch, the key is not yet fully inserted
        elif depth < len(key) - 1:
            node.mid = self._put(node.mid, key, value, depth + 1)

        # Middle branch, we've reached the end of the key, store the value
        else:
            node.value = value

        return node

    def contains(self, key):
        """
        Checks if the TST contains the given key.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key is in the TST, False otherwise.
        """
        return self.get(key) is not None

    def get(self, key):
        """
        Retrieves the value associated with the given key from the TST.

        Args:
            key (str): The key to retrieve.

        Returns:
            any: The value associated with the key, or None if the key is not found.
        """
        node = self._get(self.root, key, 0)

        if node is None:
            return None

        return node.value

    def _get(self, node, key, depth):
        """
        Recursive helper method to retrieve the value associated with the given key.

        Args:
            node (TST.Node): The current node in the TST.
            key (str): The key to retrieve.
            depth (int): The current depth in the TST.

        Returns:
            TST.Node: The node associated with the key, or None if the key is not found.
        """

        # Base case
        if node is None:
            return None

        # Recursive Exploration:
        char = key[depth]

        # Left branch
        if char < node.char:
            return self._get(node.left, key, depth)

        # Right branch
        elif char > node.char:
            return self._get(node.right, key, depth)

        # Middle branch: Traverse middle if the character matches and the key is not yet fully completed
        elif depth < len(key) - 1:
            return self._get(node.mid, key, depth + 1)

        # Middle branch: If we've reached the end of the key, return the node
        else:
            return node

    def __bool__(self):
        """
        Checks if the TST is empty.

        Returns:
            bool: True if the TST is not empty, False otherwise.
        """
        return self.root is not None

    def keys(self):
        """
        Returns all keys in the TST.

        Returns:
            list: A list of all keys in the TST.
        """
        return self.keys_with_prefix("")

    def keys_with_prefix(self, prefix):
        """
        Returns all keys in the TST that start with the given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            list: A list of keys that start with the given prefix.
        """
        queue = []

        if prefix == "":
            node_prefix = self.root
        else:
            node_prefix = self._get(self.root, prefix, 0)
        
        self._collect(node_prefix, prefix[0:-1], queue)
        return queue

    def _collect(self, node, prefix, queue):
        """
        Helper method to collect all keys in the TST with the given prefix.

        Args:
            node (TST.Node): The current node in the TST.
            prefix (str): The prefix associated with the current node.
            queue (list): The queue to collect the keys.
        """

        # The key does not exist in the TST
        if node is None:
            return

        # Recursively explore the TST in order:
        # Left branch
        self._collect(node.left, prefix, queue)

        # The node contains a value, add to the queue
        if node.value is not None:
            queue.append(prefix + node.char)

        # Middle branch
        self._collect(node.mid, prefix + node.char, queue)

        # Right branch
        self._collect(node.right, prefix, queue)

    def delete(self, key):
        """
        Deletes a key from the TST.

        Args:
            key (str): The key to delete.
        """
        if self.contains(key):
            self.size -= 1
            self.root = self._delete(self.root, key, 0)

    def _delete(self, node, key, depth):
        """
        Helper method to delete a key from the TST.

        Args:
            node (TST.Node): The current node in the TST.
            key (str): The key to delete.
            depth (int): The current depth in the TST.

        Returns:
            TST.Node: The updated node, or None if the key does not exist.
        """

        # The key does not exist in the TST
        if node is None:
            return None

        char = key[depth]

        # Left branch
        if char < node.char:
            node.left = self._delete(node.left, key, depth)

        # Right branch
        elif char > node.char:
            node.right = self._delete(node.right, key, depth)

        # Middle branch
        elif depth < len(key) - 1:
            node.mid = self._delete(node.mid, key, depth + 1)

        else:
            # We've reached the node where the value is stored
            node.value = None

        # Cleanup:

        # If the current node has a non-None value or any non-None children, return the node.
        if node.value is not None or node.left is not None or node.mid is not None or node.right is not None:
            return node

        # If the node has no value and no children,
        # return None to delete the reference to the node.
        return None

    def keys_that_match(self, pattern):
        """
        Retrieves all keys that match the specified pattern.
        The keys returned will have the same length as the given pattern.

        Args:
            pattern (str): The pattern to match, where "." serves as a wildcard that can match any character.

        Returns:
            list: A list of keys that match the specified pattern.
        """
        queue = []
        self._collect2(self.root, "", pattern, queue)
        return queue

    def _collect2(self, node, prefix, pattern, queue):
        """
        Helper method to collect all keys that match the given pattern.

        Args:
            node (TST.Node): The current node in the TST.
            prefix (str): The prefix associated with the current node.
            pattern (str): The pattern to match.
            queue (list): The queue to collect the matching keys.
        """

        # (Base case) The key does not exist in the TST
        if node is None:
            return

        depth = len(prefix)
        char = pattern[depth]

        # Left branch
        if char == "." or char < node.char:
            self._collect2(node.left, prefix, pattern, queue)

        # Middle branch
        if char == "." or char == node.char:
            if depth == len(pattern) - 1:
                queue.append(prefix + node.char)
                return
            else:
                self._collect2(node.mid, prefix + node.char, pattern, queue)

        # Right branch
        if char == "." or char > node.char:
            self._collect2(node.right, prefix, pattern, queue)

    def longest_prefix_of(self, string):
        """
        Returns the longest prefix of the given string that exists in the TST.

        Args:
            string (str): The input string to search for the longest prefix.

        Returns:
            str: The longest prefix of the input string that exists in the TST.
        """
        length = self._search(self.root, string, 0, 0)
        return string[:length]

    def _search(self, node, string, depth, length):
        """
        Helper method to find the length of the longest prefix of the given string.

        Args:
            node (TST.Node): The current node in the TST.
            string (str): The input string to search for.
            depth (int): The current depth in the TST.
            length (int): The length of the current longest prefix found.

        Returns:
            int: The length of the longest prefix of the input string that exists in the TST.
        """

        # Base cases
        if node is None:
            return length

        if depth == len(string):
            return length

        char = string[depth]

        if node.value is not None and node.char == char:
            length = depth + 1  # Updates length

        # Recursive Exploration:
        # Left branch
        if char < node.char:
            return self._search(node.left, string, depth, length)

        # Right branch
        elif char > node.char:
            return self._search(node.right, string, depth, length)
        
        # Middle branch
        else:
            return self._search(node.mid, string, depth + 1, length)


def main():
    """Main function to demonstrate the usage of the TST class."""

    # Initialize the TST
    tst = TST()

    # Add keys and values to the TST
    tst.put("cat", "animal")
    tst.put("car", "vehicle")
    tst.put("cart", "item")
    tst.put("dog", "animal")

    # Check methods
    print("All keys:", tst.keys())  # Output: ['car', 'cart', 'cat', 'dog']
    print("Keys with prefix 'car':", tst.keys_with_prefix("car"))  # Output: ['car', 'cart']
    print("Keys that match pattern '.a.':", tst.keys_that_match(".a.")) # Output: ['car', 'cat']
    print("Longest prefix of 'cartoon':", tst.longest_prefix_of("cartoon")) # Output: cart


if __name__ == "__main__":
    main()