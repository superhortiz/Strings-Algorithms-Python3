import networkx as nx
import matplotlib.pyplot as plt


class Digraph:
    """
    Represents a directed graph using adjacency lists.
    """

    def __init__(self, number_of_vertices):
        """
        Initializes the directed graph with the given number of vertices.
        
        Args:
            number_of_vertices (int): The number of vertices in the graph.
        """

        self.number_of_vertices = number_of_vertices
        self.adjacency_lists = {vertex: set() for vertex in range(self.number_of_vertices)}

    @property
    def number_of_edges(self):
        """
        Returns the number of edges in the graph.
        
        Returns:
            int: The total number of edges.
        """

        return sum([len(adjacency_list) for adjacency_list in self.adjacency_lists.values()])

    def add_edge(self, vertex_v, vertex_w):
        """
        Adds a directed edge from vertex_v to vertex_w.
        
        Args:
            vertex_v (int): The source vertex.
            vertex_w (int): The destination vertex.
        """

        self.adjacency_lists[vertex_v].add(vertex_w)

    def remove_edge(self, vertex_v, vertex_w):
        """
        Removes the directed edge from vertex_v to vertex_w.
        
        Args:
            vertex_v (int): The source vertex.
            vertex_w (int): The destination vertex.
        """

        self.adjacency_lists[vertex_v].remove(vertex_w)

    def adjacents(self, vertex_v):
        """
        Returns the vertices adjacent to the given vertex.
        
        Args:
            vertex_v (int): The vertex.
        
        Returns:
            set: A set of adjacent vertices.
        """

        return self.adjacency_lists[vertex_v]

    def degree(self, vertex_v):
        """
        Returns the out-degree of the given vertex.
        
        Args:
            vertex_v (int): The vertex.
        
        Returns:
            int: The out-degree of the vertex.
        """

        return len(self.adjacency_lists[vertex_v])

    def max_degree(self):
        """
        Returns the maximum out-degree of any vertex in the graph.
        
        Returns:
            int: The maximum out-degree.
        """

        return max([len(adjacency_list) for adjacency_list in self.adjacency_lists.values()])

    def average_degree(self):
        """
        Returns the average out-degree of the vertices in the graph.
        
        Returns:
            float: The average out-degree.
        """

        return self.number_of_edges / self.number_of_vertices

    def number_self_loops(self):
        """
        Returns the number of self-loops in the graph.
        
        Returns:
            int: The number of self-loops.
        """

        count = 0
        for vertex_v in self.adjacency_lists.keys():
            for vertex_w in self.adjacency_lists[vertex_v]:
                if vertex_v == vertex_w:
                    count += 1
        return count

    @classmethod
    def from_file(cls, file_path):
        """
        Creates a Digraph instance from a file.
        
        Args:
            file_path (str): The path to the file containing the graph data.
        
        Returns:
            Digraph: An instance of the Digraph class.
        """
        with open(file_path, 'r') as file:
            # Read the first two lines
            number_of_vertices = int(file.readline().rstrip())

            # Print the first two lines
            digraph = cls(number_of_vertices)

            # Iterate over the rest of the file
            for line in file:
                vertex_v, vertex_w = map(int, line.rstrip().split())
                digraph.add_edge(vertex_v, vertex_w)

            return digraph

    @classmethod
    def reverse_graph(cls, graph):
        """
        Creates a new digraph which is the reverse of the given graph.
        
        Args:
            graph (Digraph): The original digraph.
        
        Returns:
            Digraph: A new digraph where all edges are reversed.
        """

        reversed_graph = cls(graph.number_of_vertices)

        for vertex_v, set_vertices_w in graph.adjacency_lists.items():
            for vertex_w in set_vertices_w:
                reversed_graph.add_edge(vertex_w, vertex_v)

        return reversed_graph

    def to_networkx_graph(self):
        """
        Converts the graph to a NetworkX directed graph.
        
        Returns:
            networkx.DiGraph: A NetworkX directed graph representing the same graph.
        """

        # Create an empty undirected digraph using NetworkX
        digraph = nx.DiGraph()

        # Add Edges to NetworkX Graph
        for vertex_v in range(self.number_of_vertices):
            for vertex_w in self.adjacency_lists[vertex_v]:
                digraph.add_edge(vertex_v, vertex_w)
        return digraph
