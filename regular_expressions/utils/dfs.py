class DirectedDFS:
    """
    Implements Depth-First Search (DFS) for a directed graph.
    """

    def __init__(self, graph, sources):
        """
        Initializes the DirectedDFS object and performs DFS from the source vertex.
        
        Args:
            graph (Digraph): The directed graph to perform DFS on.
            sources (set): The source vertex from which to start the DFS.
        """

        self.marked = [False] * graph.number_of_vertices
        self.edge_to = [None] * graph.number_of_vertices

        # Convert sources to a set in case is an int instance
        if isinstance(sources, int):
            sources = {sources}

        for source in sources:
            if not self.marked[source]:
                self._dfs(graph, source)

    def _dfs(self, graph, vertex):
        """
        Recursively performs DFS starting from the given vertex.
        
        Args:
            graph (Digraph): The directed graph to perform DFS on.
            vertex (int): The current vertex being visited.
        """

        self.marked[vertex] = True
        for adjacent in graph.adjacency_lists[vertex]:
            if not self.marked[adjacent]:
                self._dfs(graph, adjacent)
                self.edge_to[adjacent] = vertex

    def has_path_to(self, vertex):
        """
        Checks if there is a path from the source vertex to the given vertex.
        
        Args:
            vertex (int): The target vertex.
        
        Returns:
            bool: True if there is a path, False otherwise.
        """

        return self.marked[vertex]

    def path_to(self, vertex):
        """
        Returns the path from the source vertex to the given vertex, if it exists.
        
        Args:
            vertex (int): The target vertex.
        
        Returns:
            str: A string representation of the path from the source to the target.
            None: If no path exists.
        """

        if not self.has_path_to(vertex):
            return None

        path = []
        current_vertex = vertex

        while current_vertex is not None:
            path.append(current_vertex)
            current_vertex = self.edge_to[current_vertex]
        return ' -> '.join(str(vertex) for vertex in reversed(path))


def main():
    """
    Main function to read a directed graph from a file, perform DFS, and print the path information.
    """

    FILE_PATH = "data/digraph.txt"
    digraph = Digraph.from_file(FILE_PATH)
    source = 7
    vertex = 1
    dfs = DirectedDFS(digraph, source)
    print(f"Is there a path from {source} to {vertex}? {dfs.has_path_to(vertex)}")
    print(f"Path from {source} to {vertex}: {dfs.path_to(vertex)}")


if __name__ == "__main__":
    main()