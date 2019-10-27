from lib.montecarlo.nodes import Node


class Tree:
    def __init__(self, root_node):
        self.root = root_node

    def best_move(self, num_simulations):
        """
        Selects the best move.
        :param num_simulations: int: the number of simulations to run
        :return: Node: represents the best move and game state
        """
        for _ in range(0, num_simulations):
            # Select leaf node to run a simulation on
            leaf = self.select()

            # Expand leaf node and select child to rollout.
            child_node = leaf.expand()

            # Rollout
            simulation_result = child_node.rollout()

            # Backpropogate
            child_node.backpropagate(simulation_result)

        sorted_children = sorted(self.root.children,
                                 key=lambda child: child.visit_count,
                                 reverse=True)
        return sorted_children[0]

    def select(self):
        """
        Select node to expand.
        :return: Node: leaf node to expand.
        """
        current_node = self.root

        # While this node has children (not a leaf node)
        while current_node.children:
            current_node = current_node.promising_child()

        return current_node
