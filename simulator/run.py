from simulator.util import print_board
from lib.montecarlo.tree import Tree
from lib.montecarlo.nodes import Node
from lib.montecarlo.game import GameState, Move


class Player:
    def __init__(self, player_num):
        self.player_num = player_num

    def get_move(self, board):
        root = Node(state=board)
        mcts = Tree(root)

        best_node = mcts.best_move(10)
        if best_node is None:
            return None

        move = best_node.transition_move
        return [move.row, move.col]


class Simulator:
    def __init__(self):
        initial_board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 2, 0, 0, 0],
            [0, 0, 0, 2, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.board = GameState(1, initial_board)
        self.p1 = Player(1)
        self.p2 = Player(2)
        self.turn = 1

    def update_board(self, row, col, player):
        move = Move(row, col, player)
        self.board = self.board.move(move)

    def play_game(self):
        while not self.board.game_over():
            if self.turn == 1:
                move = self.p1.get_move(self.board)

                if move is None:
                    self.update_board(None, None, 1)
                    print("Player 1 has no valid moves.")
                    self.turn = 2
                else:
                    self.update_board(move[0], move[1], 1)
                    print(f"Player 1 played at [{move[0]}, {move[1]}]")
                    print_board(self.board.board)
                    self.turn = 2
            else:
                move = self.p2.get_move(self.board)

                if move is None:
                    self.update_board(None, None, 1)
                    print("Player 2 has no valid moves.")
                    self.turn = 1
                else:
                    self.update_board(move[0], move[1], 2)
                    print(f"Player 2 played at [{move[0]}, {move[1]}]")
                    print_board(self.board.board)
                    self.turn = 1

        result = self.board.game_result()
        print(f"Winner: Player {result}")


if __name__ == '__main__':
    sim = Simulator()
    sim.play_game()
