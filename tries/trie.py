class TrieST:
    """
    A Trie (Prefix Tree) data structure implementation for extended ASCII.
    """
    R = 256  # For extended ASCII

    class Node:
        """
        A node in the Trie.
        """
        def __init__(self):
            """Initializes a node with a value and an array of children."""
            self.value = None
            self.next = [None] * TrieST.R

    def __init__(self):
        """Initializes the root node and the size of the trie."""
        self.root = TrieST.Node()
        self.size = 0

    def put(self, key, value):
        """
        Inserts a key-value pair into the trie.

        Args:
            key (str): The key to insert.
            value: The value associated with the key.
        """
        if not self.contains(key):
            self.size += 1
        self.root = self._put(self.root, key, value, 0)

    def _put(self, node, key, value, depth):
        """
        Helper method to insert a key-value pair into the trie.

        Args:
            node (TrieST.Node): The current node in the trie.
            key (str): The key to insert.
            value: The value associated with the key.
            depth (int): The current depth in the trie.

        Returns:
            TrieST.Node: The updated node.
        """
        if node is None:
            node = TrieST.Node()

        if depth == len(key):
            node.value = value
            return node

        char = ord(key[depth])
        node.next[char] = self._put(node.next[char], key, value, depth + 1)
        return node

    def contains(self, key):
        """
        Checks if a key is in the trie.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key is in the trie, False otherwise.
        """
        return self.get(key) is not None

    def get(self, key):
        """
        Retrieves the value associated with the given key.

        Args:
            key (str): The key to retrieve.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        node = self._get(self.root, key, 0)

        if node is None:
            return None

        return node.value

    def _get(self, node, key, depth):
        """
        Helper method to retrieve the node associated with the given key.

        Args:
            node (TrieST.Node): The current node in the trie.
            key (str): The key to retrieve.
            depth (int): The current depth in the trie.

        Returns:
            TrieST.Node: The node associated with the key, or None if not found.
        """
        if node is None:
            return None

        if depth == len(key):
            return node

        char = ord(key[depth])
        return self._get(node.next[char], key, depth + 1)

    def delete(self, key):
        """
        Deletes a key from the trie.

        Args:
            key (str): The key to delete.
        """
        if self.contains(key):
            self.size -= 1
            self.root = self._delete(self.root, key, 0)

    def _delete(self, node, key, depth):
        """
        Helper method to delete a key from the trie.

        Args:
            node (TrieST.Node): The current node in the trie.
            key (str): The key to delete.
            depth (int): The current depth in the trie.

        Returns:
            TrieST.Node: The updated node, or None if the key does not exist.
        """

        # The key does not exist in the trie
        if node is None:
            return None

        # We've reached the node where the value is stored
        if depth == len(key):
            # Set the value of this node to None
            node.value = None

        # We're not yet at the end of the key, proceed to the next character
        else:
            char = ord(key[depth])
            node.next[char] = self._delete(node.next[char], key, depth + 1)

        # Cleanup

        # If the current node has a non-None value, return the node.
        # This means there are still other keys stored here or this is the root node.

        if node.value is not None or node == self.root:
            return node

        # Check if the current node has any non-None children.
        # If it does, return the node.
        for node_next in node.next:
            if node_next is not None:
                return node

        # If the node has no value and no children,
        # return None to delete the reference to the node.
        return None

    def __bool__(self):
        """
        Checks if the trie is empty.

        Returns:
            bool: True if the trie is not empty, False otherwise.
        """
        if self.root.value is not None:
            return True

        for node_next in self.root.next:
            if node_next is not None:
                return True

        return False

    def keys(self):
        """
        Returns all keys in the trie.

        Returns:
            list: A list of all keys in the trie.
        """
        return self.keys_with_prefix("")

    def keys_with_prefix(self, prefix):
        """
        Returns all keys in the trie that start with the given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            list: A list of keys that start with the given prefix.
        """
        queue = []
        node_prefix = self._get(self.root, prefix, 0)
        self._collect(node_prefix, prefix, queue)
        return queue

    def _collect(self, node, prefix, queue):
        """
        Helper method to collect all keys in the trie with the given prefix.

        Args:
            node (TrieST.Node): The current node in the trie.
            prefix (str): The prefix associated with the current node.
            queue (list): The queue to collect the keys.
        """

        # The key does not exist in the trie
        if node is None:
            return

        # The node contains a value, add to the queue
        if node.value is not None:
            queue.append(prefix)

        # Recursively explore the trie
        for i, node_next in enumerate(node.next):
            self._collect(node_next, prefix + chr(i), queue)

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
            node (TrieST.Node): The current node in the trie.
            prefix (str): The prefix associated with the current node.
            pattern (str): The pattern to match.
            queue (list): The queue to collect the matching keys.
        """

        # (Base case) The key does not exist in the trie
        if node is None:
            return

        # (Base case) We have reached the end of the pattern
        depth = len(prefix)
        if depth == len(pattern):
            if node.value is not None:
                queue.append(prefix)
            return

        # Recursive Exploration
        next_char = pattern[depth]
        for i, node_next in enumerate(node.next):
            if next_char == '.' or next_char == chr(i):
                self._collect2(node_next, prefix + chr(i), pattern, queue)

    def longest_prefix_of(self, string):
        """
        Returns the longest prefix of the given string that exists in the trie.

        Args:
            string (str): The input string to search for the longest prefix.

        Returns:
            str: The longest prefix of the input string that exists in the trie.
        """
        length = self._search(self.root, string, 0, 0)
        return string[:length]

    def _search(self, node, string, depth, length):
        """
        Helper method to find the length of the longest prefix of the given string.

        Args:
            node (TrieST.Node): The current node in the trie.
            string (str): The input string to search for.
            depth (int): The current depth in the trie.
            length (int): The length of the current longest prefix found.

        Returns:
            int: The length of the longest prefix of the input string that exists in the trie.
        """

        # Base cases
        if node is None:
            return length
        if node.value is not None:
            length = depth  # Updates length
        if depth == len(string):
            return length

        # Recursive Exploration
        char = ord(string[depth])
        return self._search(node.next[char], string, depth + 1, length)


def main():
    """Main function to demonstrate the usage of the TrieST class."""

    # Initialize the trie
    trie = TrieST()

    # Add keys and values to the trie
    trie.put("cat", "animal")
    trie.put("car", "vehicle")
    trie.put("cart", "item")
    trie.put("dog", "animal")

    # Check methods
    print("All keys:", trie.keys())  # Output: ['car', 'cart', 'cat', 'dog']
    print("Keys with prefix 'car':", trie.keys_with_prefix("car"))  # Output: ['car', 'cart']
    print("Keys that match pattern '.a.':", trie.keys_that_match(".a.")) # Output: ['car', 'cat']
    print("Longest prefix of 'cartoon':", trie.longest_prefix_of("cartoon")) # Output: cart


if __name__ == "__main__":
    main()