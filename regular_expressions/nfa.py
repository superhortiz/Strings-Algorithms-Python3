from utils.digraph import Digraph
from utils.dfs import DirectedDFS


class NFA:
    """
    A class to represent a Non-deterministic Finite Automaton (NFA).

    Attributes:
        regexp (str): The regular expression.
        length_regexp (int): The length of the regular expression.
        graph (Digraph): The digraph representing the NFA.
    """

    def __init__(self, regexp):
        """
        Initializes the NFA with the given regular expression.

        Args:
            regexp (str): The regular expression.
        """
        self.regexp = regexp
        self.length_regexp = len(regexp)
        self.graph = self.build_digraph()

    def recognizes(self, text):
        """
        Determines if the NFA recognizes the given text.

        Args:
            text (str): The text to be recognized by the NFA.

        Returns:
            bool: True if the NFA recognizes the text, False otherwise.
        """

        # program_counter: Set of all possible states that the NFA could be in given the current state
        program_counter = set()

        # Build DFS with source = 'state 0'
        dfs = DirectedDFS(self.graph, 0)

        for vertex in range(self.graph.number_of_vertices):

            # We put in program_counter all the states reachable from 'state 0'
            if dfs.has_path_to(vertex):
                program_counter.add(vertex)

        # Iterate over the string "text"
        for char in text:

            # Set of states reachable after scanning past char
            states = set()

            # Iterate over the current reachable states
            for vertex in program_counter:

                # Not necessarily a match (regexp needs to match full text).
                # However, the input text may still have more characters to process, then we just move to the next steps.
                if vertex == self.length_regexp:
                    continue

                # We have a match between text and regex
                if self.regexp[vertex] == char or self.regexp[vertex] == '.':

                    # Include the next state in the set to consider in the next iteration
                    states.add(vertex + 1)

            # Builds DFS using a set of sources
            dfs = DirectedDFS(self.graph, states)
            program_counter = set()

            # We put in program_counter all the states reachable from 'states'
            for vertex in range(self.graph.number_of_vertices):
                if dfs.has_path_to(vertex):
                    program_counter.add(vertex)

        # Check if we have reached the accept state
        for vertex in program_counter:
            if vertex == self.length_regexp:
                return True
        return False


    def build_digraph(self):
        """
        Builds the epsilon transition digraph for the NFA.

        Returns:
            Digraph: The digraph representing the NFA.
        """
        graph = Digraph(self.length_regexp + 1)  # M + 1 to have an extra node for accept state
        operators = []  # Stack to keep track of the operators '(', ')' and '|'

        for i in range(self.length_regexp):

            # We found '(' or '|', add the index 'i' to the stack 'operators'
            left_parentheses = i
            if self.regexp[i] == '(' or self.regexp[i] == '|':
                operators.append(i)

            # We found a closing parenthesis ')'
            elif self.regexp[i] == ')':
                or_index = operators.pop()

                # We are closing parentheses which includes '|'
                if self.regexp[or_index] == '|':

                    # Update 'left_parentheses' if '|' was found
                    left_parentheses = operators.pop()

                    # Add two ε-transition edges for each '|' operator.
                    graph.add_edge(left_parentheses, or_index + 1)
                    graph.add_edge(or_index, i)

                # No '|' found, it corresponds to a '('
                else:
                    left_parentheses = or_index

            # Closure needs 1-character lookahead, so we we just go to length_regexp-1
            if i < self.length_regexp - 1 and self.regexp[i + 1] == '*':

                # Add two ε-transition edges for each '*' operator
                graph.add_edge(left_parentheses, i + 1)
                graph.add_edge(i + 1, left_parentheses)

            # Add ε-transition edges for '(', '*', and ')'
            if self.regexp[i] == '(' or self.regexp[i] == '*' or self.regexp[i] == ')':
                graph.add_edge(i, i + 1)

        return graph


def main():
    """
    Main function to test the compression and expansion of a sample ASCII file.
    """
    pattern = "((A*B|AC)D)"
    text1 = "AAAABD"
    text2 = "ABAB."
    text3 = "ABDD"
    nfa = NFA(pattern)
    print(f"Pattern: {pattern}, Text: {text1}, Recognized: {nfa.recognizes(text1)}")  # Expected: True
    print(f"Pattern: {pattern}, Text: {text2}, Recognized: {nfa.recognizes(text2)}")  # Expected: False
    print(f"Pattern: {pattern}, Text: {text3}, Recognized: {nfa.recognizes(text3)}")  # Expected: False


if __name__ == "__main__":
    main()