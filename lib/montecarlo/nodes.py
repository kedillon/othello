import random

import numpy as np
from lib.montecarlo.util import other_player


class Node:
    def __init__(self, state, parent=None, transition_move=None):
        """
        Initialize the node.
        :param state: NodeState object. Represents the state of the node.
        :param parent: Node object. This node's parent.
        :param transition_move: Move object. Represents the move that
               transitioned parent state to this state.
        """
        self.state = state
        self.parent = parent
        self.children = []

        self.transition_move = transition_move
        self.visit_count = 0
        self.win_score = 0

    @property
    def fully_expanded(self):
        """
        Checks if node is fully expanded.
        :return: bool.
        """
        return len(self.untried_moves) == 0

    def expand(self):
        """
        Expand a leaf node and choose a random child to rollout.
        :return: Node: Represents node to rollout.
        """
        if self.children:
            raise Exception("Cannot expand an expanded node.")

        for move in self.state.get_legal_moves():
            # Create a child node with updated state after move was made,
            # valid parent, and transition move
            child = Node(self.state.move(move),
                         parent=self,
                         transition_move=move)
            self.children.append(child)

        if not self.children:
            return None

        return random.choice(self.children)

    def backpropagate(self, game_result):
        """
        Updates visit and win values for all nodes in path.
        :param game_result: int: result of the game after rollout.
        """
        self.visit_count += 1
        # other_player would have created this state
        # Add to other player's wins
        if game_result == other_player(self.state.next_player):
            self.win_score += 1
        # Game ended in a Draw
        elif game_result == 0:
            self.win_score += 0.5

        # Backpropogate from parent node
        if self.parent:
            self.parent.backpropagate(game_result)

    def promising_child(self, c=1.4):
        """
        Use upper confidence bound (UTC) to choose next node to explore.
        Source: https://en.wikipedia.org/wiki/Monte_Carlo_tree_search

        :param c: double: exploration parameter
        :return: Node: next node to explore/expand.
        """
        weights = [
            (child.win_score / child.visit_count) + c * np.sqrt(
                np.log(self.visit_count) / child.visit_count
            )
            for child in self.children
        ]
        return self.children[np.argmax(weights)]

    def rollout(self):
        """
        Rollout from this node to find game result.
        :return: int: Represents the game result. 1, 2, or None
        """
        if self.state.game_over():
            return self.state.game_result()

        legal_moves = self.state.get_legal_moves()
        random_move = random.choice(legal_moves)
        node = Node(self.state.move(random_move))
        return node.rollout()


