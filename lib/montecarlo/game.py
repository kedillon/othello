"""Othello game representation."""
from lib.montecarlo.util import in_bounds, other_player, increment_row_col


class Move:
    def __init__(self, row, col, player):
        self.player = player
        self.row = row
        self.col = col


class GameState:
    def __init__(self, next_player, board_state):
        self.next_player = next_player
        self.board = board_state

    def game_result(self):
        """
        Returns player who won (1 or 2) or None if winner is unknown.
        :return: int: winning player
        """
        pass

    def winner_exists(self):
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
        pass

    def move_is_legal(self, action):
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

    def get_legal_moves(self):
        """
        Gets legal moves from this state.
        :return: list: Move objects
        """

        pass
