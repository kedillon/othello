"""Othello game representation."""
import numpy as np

from lib.montecarlo.util import in_bounds, other_player, increment_row_col
from mctspy.games.common import TwoPlayersAbstractGameState, AbstractGameAction


class OthelloMove(AbstractGameAction):
    def __init__(self, row, col, player):
        self.player = player
        self.row = row
        self.col = col

    def __str__(self):
        return f"Player {self.player}: [{self.row}, {self.col}]"


class OthelloGameState(TwoPlayersAbstractGameState):
    def __init__(self, next_to_move, state):
        """
        Initialize the game.
        :param next_to_move: int: Represents the player.
        :param state: numpy array: Represents the current board state
        """
        self.next_to_move = next_to_move
        self.board = state

    def game_result(self):
        """
        Returns player who won (1 or 2) or None if winner is unknown.
        :return: int: winning player
        """
        if not self.get_legal_actions():
            return other_player(self.next_to_move)
        elif not self.get_player_legal_actions(other_player(self.next_to_move)):
            return self.next_to_move
        return None

    def is_game_over(self):
        """
        Determine if a winner exists and the game is over.
        :return: bool
        """
        return self.game_result() is not None

    def move(self, action):
        """
        Make a move and return updated game state.
        :param action: Move: represents a move
        :return: GameState: updated game state
        """
        if not self.is_move_legal(action):
            raise Exception("Illegal move")
            return None
        new_state = self.board.copy()
        new_state[action.row][action.col] = action.player

        # Checks that piece was placed by opponent
        def promising(r, c):
            if in_bounds(r, c) and self.board[r][c] == other_player(action.player):
                return True
            return False

        def flip_in_direction(direction):
            row, col = increment_row_col(action.row, action.col, direction)
            if promising(row, col):
                flips = []
                while promising(row, col):
                    flips.append([row, col])
                    row, col = increment_row_col(row, col, direction)
                if in_bounds(row, col) and self.board[row][col] == action.player:
                    for location in flips:
                        new_state[location[0]][location[1]] = action.player

        flip_in_direction("N")
        flip_in_direction("S")
        flip_in_direction("E")
        flip_in_direction("W")
        flip_in_direction("NE")
        flip_in_direction("NW")
        flip_in_direction("SE")
        flip_in_direction("SW")

        return OthelloGameState(other_player(action.player), new_state)

    def is_move_legal(self, action):
        """
        Check if a move is legal.
        :param action: Move: represents a move
        :return: bool
        """
        # Check that action is in bounds and empty square
        if not in_bounds(action.row, action.col):
            return False
        if self.board[action.row][action.col] != 0:
            return False

        # Checks that piece was placed by opponent
        def promising(r, c):
            if in_bounds(r, c) and self.board[r][c] == other_player(action.player):
                return True
            return False

        def legal_move_in_direction(direction):
            row, col = increment_row_col(action.row, action.col, direction)
            if promising(row, col):
                while promising(row, col):
                    row, col = increment_row_col(row, col, direction)
                if not in_bounds(row, col) or self.board[row][col] != action.player:
                    return False
                # We have followed a path of opponent pieces and arrived an another of our pieces
                return True
            return False

        if legal_move_in_direction("N") or \
                legal_move_in_direction("S") or \
                legal_move_in_direction("E") or \
                legal_move_in_direction("W") or \
                legal_move_in_direction("NE") or \
                legal_move_in_direction("NW") or \
                legal_move_in_direction("SE") or \
                legal_move_in_direction("SW"):
            return True
        else:
            return False

    def get_player_legal_actions(self, player):
        """
        Gets legal moves from this state.
        :return: list: Move objects
        """
        valid_moves = []

        for row in range(len(self.board)):
            for col in range(8):
                move = OthelloMove(row, col, player)
                if self.is_move_legal(move):
                    valid_moves.append(move)

        return valid_moves

    def get_legal_actions(self):
        return self.get_player_legal_actions(self.next_to_move)
