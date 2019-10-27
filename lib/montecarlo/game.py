"""Othello game representation."""
import copy

from lib.montecarlo.util import in_bounds, other_player, increment_row_col


class Move:
    def __init__(self, row, col, player):
        self.player = player
        self.row = row
        self.col = col

    def __str__(self):
        return f"Player {self.player}: [{self.row}, {self.col}]"

    def __repr__(self):
        return f"Player {self.player}: [{self.row}, {self.col}]"

    def __eq__(self, other):
        return self.player == other.player and \
               self.row == other.row and \
               self.col == other.col


class GameState:
    def __init__(self, next_player, board_state):
        """
        Initialize the game.
        :param next_player: int: next player to play. (i.e. This player is
               presented with and must consider this board state.)
        :param board_state: 2D list: Represents the board. Includes 0, 1, 2.
        """
        self.next_player = next_player
        self.board = board_state

    def game_result(self):
        """
        Returns player who won (1 or 2) or None if winner is unknown.
        :return: int: winning player
        """
        next_player_legal_moves = self.get_player_legal_moves(self.next_player)
        other_legal_moves = self.get_player_legal_moves(other_player(self.next_player))

        # Neither player can make moves
        if not next_player_legal_moves and not other_legal_moves:
            total_next = sum(row.count(self.next_player) for row in self.board)
            total_other = sum(row.count(other_player(self.next_player)) for row in self.board)

            if total_next > total_other:
                return self.next_player
            elif total_other > total_next:
                return other_player(self.next_player)
            else:
                return 0
        return None

    def game_over(self):
        """
        Determine if the game is over.
        :return: bool
        """
        return self.game_result() is not None

    def move(self, action):
        """
        Make a move and return updated game state.
        :param action: Move: represents a move
        :return: GameState: updated game state
        """
        # If no move was made by player, copy state and switch player.
        if action.row is None and action.col is None:
            new_state = copy.deepcopy(self.board)
            return GameState(other_player(action.player), new_state)

        if not self.move_is_legal(action):
            raise Exception("Illegal move")
            return None
        new_state = copy.deepcopy(self.board)
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

        return GameState(other_player(action.player), new_state)

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
            """
            Check that piece at row r and column c was played by opponent.
            :param r: int: Represents the row.
            :param c: int: Represents the column.
            :return: bool. True if piece was placed by opponent, False otherwise.
            """
            if in_bounds(r, c) and \
                    self.board[r][c] == other_player(action.player):
                return True
            return False

        def legal_move_in_direction(direction):
            """
            Check that a move is legal in a certain direction.
            :param direction: string: Represents the direction.
                   One of: ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]
            :return: bool: True if move is legal in given direction, False otherwise.
            """
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

    def get_player_legal_moves(self, player):
        """
        Gets legal moves from this state.
        :return: list: Move objects
        """
        valid_moves = []

        for row in range(len(self.board)):
            for col in range(8):
                move = Move(row, col, player)
                if self.move_is_legal(move):
                    valid_moves.append(move)

        return valid_moves

    def get_legal_moves(self):
        """
        Get legal moves for self.next_player.
        :return: list: Move objects
        """
        return self.get_player_legal_moves(self.next_player)

