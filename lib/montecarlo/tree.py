"""The mcts used to identify promising moves."""
import numpy as np

class Tree:
    def __init__(self, root_node):
        """
        Initialize the tree with a root node.
        :param root_node: Node: root of this tree. Usually the initial board.
        """
        self.root = root_node

    def best_move(self, num_simulations, model):
        """
        Selects the best move.
        :param num_simulations: int: the number of mcts simulations to run
        :return: Node, list: the best move at this game state, the number of
                 mcts visits to each square on the board (all possible moves
                 including illegal).
        """
        for _ in range(0, num_simulations):
            # Select leaf node to run a simulation on using UCB
            leaf = self.select()

            # Use vanilla monte carlo tree search
            if model is None:
                # Expand this node and choose a random child
                leaf.expand_mcts()
                child_node = leaf.random_child()

                # Child node will be none if this leaf node results
                # in no valid moves
                if child_node:
                    # Rollout
                    simulation_result = child_node.rollout()
                    # Backpropogate
                    child_node.backpropagate(simulation_result)

            # Use specified machine learning model
            else:
                # Expand this leaf node using the model, get the expected value
                # of a win/loss, and assign priors to this node's children.
                value = leaf.expand(model)
                # Backpropagate the expected value from this node.
                leaf.backpropagate(value)

        # TODO: In future iterations, handle a "pass" move.
        if not self.root.children:
            return None, None
        #
        #
        # sorted_children = sorted(self.root.children,
        #                          key=lambda child: child.visit_count,
        #                          reverse=True)

        # List of size 64, filled with zeros. Represents visits to squares on
        # the board. Used as part of model training data.
        all_move_visits = [0] * 64
        for child in self.root.children:
            # Sets visit_count at 1D index of move.
            idx = child.transition_move.row * 8 + child.transition_move.col
            all_move_visits[idx] = child.visit_count

        # Create probability distribution to avoid overfitting
        dist = np.array([
            float(child.visit_count)
            for child in self.root.children
        ])
        dist = dist / dist.sum()
        dist = dist ** 5
        dist = dist / dist.sum()
        # Randomly choose a node given probabilities.
        # Allows us to explore more branches of the tree
        return self.root.children[
                   np.random.choice(len(self.root.children), p=dist)
               ], all_move_visits

    def select(self):
        """
        Select node to expand.
        :return: Node: leaf node to expand.
        """
        current_node = self.root

        # Select promising children using UCB until we reach a leaf node.
        while current_node.children:
            current_node = current_node.promising_child()

        return current_node
