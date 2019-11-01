"""Othello player types."""
import random

from lib.montecarlo.tree import Tree
from lib.montecarlo.nodes import Node


class RandomPlayer:
    """A player that uses random selection of legal moves."""
    def __init__(self, player_num):
        self.player_num = player_num

    def get_move(self, board):
        legal = board.get_player_legal_moves(self.player_num)
        move = random.choice(legal)
        return [move.row, move.col], None


class ModelPlayer:
    """A player that uses a machine learning model."""
    def __init__(self, player_num, model):
        self.player_num = player_num
        self.model = model

    def get_move(self, board):
        """
        Get's the player's chosen move and a list of move visits from mcts
        :param board:
        :return:
        """
        root = Node(state=board)
        mcts = Tree(root)

        best_node, all_move_visits = mcts.best_move(500, self.model)
        if best_node is None:
            return None, None

        move = best_node.transition_move
        return [move.row, move.col], all_move_visits


class MCTSPlayer:
    """A player that uses a vanilla Monte Carlo Tree Search."""
    def __init__(self, player_num):
        self.player_num = player_num

    @staticmethod
    def get_move(board):
        """
        Get's the player's chosen move and a list of move visits from mcts
        :param board: GameState: represents the state of the game
        :return: list, list: row and column, number of visits for each square
        """
        root = Node(state=board)
        mcts = Tree(root)

        best_node, all_move_visits = mcts.best_move(1300, None)
        if best_node is None:
            return None, None

        move = best_node.transition_move
        return [move.row, move.col], all_move_visits
