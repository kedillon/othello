import random

import numpy as np
from lib.montecarlo.game import Move
from lib.montecarlo.util import other_player
from lib.ml.run import evaluate_model_at_gamestate


class Node:
    def __init__(self, state, prior=0, parent=None, transition_move=None):
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
        self.prior = prior

    def expand(self, model):
        """Expand a leaf node and attach children."""
        if self.children:
            raise Exception("Cannot expand an expanded node.")

        # Evaluate the board at this state using ml model
        value, policy = evaluate_model_at_gamestate(self.state, model)

        for move in self.state.get_legal_moves():
            # Create a child node with updated state after move was made,
            # valid parent, and transition move
            child = Node(self.state.move(move),
                         parent=self,
                         transition_move=move,
                         prior=policy[move.row][move.col])
            self.children.append(child)

        # Returns value to backpropagate up the tree
        return value

    def expand_mcts(self):
        if self.children:
            raise Exception("Cannot expand an expanded node.")

        for move in self.state.get_legal_moves():
            # Create a child node with updated state after move was made,
            # valid parent, and transition move
            child = Node(self.state.move(move),
                         parent=self,
                         transition_move=move)
            self.children.append(child)

    def random_child(self):
        """
        Returns a random child of this node, or none if this
        node has no children.
        :return: Node
        """
        if not self.children:
            return None
        else:
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
        # Add 1 to denominator to avoid division by zero
        weights = [
            child.win_score / max(child.visit_count, 1) + \
            c * child.prior * np.sqrt(
                self.visit_count
            ) / (child.visit_count + 1)
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
        if not legal_moves:
            random_move = Move(None, None, self.state.next_player)
        else:
            random_move = random.choice(legal_moves)
        node = Node(self.state.move(random_move))
        return node.rollout()


