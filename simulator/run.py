import os
import json
import time

from lib.ml.run import load_model
from simulator.util import print_board
from lib.montecarlo.tree import Tree
from lib.montecarlo.nodes import Node
from lib.montecarlo.util import other_player
from lib.montecarlo.game import GameState, Move


class Player:
    def __init__(self, player_num, model_filename=None):
        self.player_num = player_num

        # Load model
        if model_filename is None:
            self.model = None
        else:
            self.model = load_model(model_filename)

    def get_move(self, board):
        """
        Get's the player's chosen move and a list of move visits from mcts
        :param board:
        :return:
        """
        root = Node(state=board)
        mcts = Tree(root)

        best_node, all_move_visits = mcts.best_move(700, self.model)
        if best_node is None:
            return None, None

        move = best_node.transition_move
        return [move.row, move.col], all_move_visits


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
        self.p1 = Player(1, "final_model")
        self.p2 = Player(2, "final_model")
        self.turn = 1

        # All game states accessed during the game.
        self.all_game_states = []

    def update_board(self, row, col, player):
        move = Move(row, col, player)
        self.board = self.board.move(move)

    def store_game_state(self, counts):
        self.all_game_states.append([self.board, counts])

    def store_game_result(self, result):
        for state in self.all_game_states:

            # Other player created this state, other player won
            if other_player(state[0].next_player) == result:
                state.append(1)
            # This player created this state, other player won
            elif state[0].next_player == result:
                state.append(0)
            else:
                state.append(0.5)

    def export_game_data(self, path):

        game_meta = [
            {
                "created_by": other_player(state[0].next_player),
                "board": state[0].board,
                "move_visits": state[1],
                "winloss": state[2]
            }
            for state in self.all_game_states
        ]

        try:
            with open(path) as infile:
                data = json.load(infile)
                data.extend(game_meta)
                print("TRAINING SET SIZE: {}".format(len(data)))

            with open(path, 'w') as outfile:
                json.dump(data, outfile)
        except:
            with open(path, 'w+') as outfile:
                json.dump(game_meta, outfile)

    def play_game(self):
        while not self.board.game_over():
            if self.turn == 1:
                move, all_move_visits = self.p1.get_move(self.board)

                if move is None:
                    self.update_board(None, None, 1)
                    print("Player 1 has no valid moves.")
                    self.turn = 2
                else:
                    # Save current state
                    self.store_game_state(all_move_visits)
                    self.update_board(move[0], move[1], 1)
                    print("Player 1 played at [{}, {}]".format(move[0], move[1]))
                    print_board(self.board.board)
                    self.turn = 2
            else:
                move, all_move_visits = self.p2.get_move(self.board)

                if move is None:
                    self.update_board(None, None, 2)
                    print("Player 2 has no valid moves.")
                    self.turn = 1
                else:
                    # Save current state
                    self.store_game_state(all_move_visits)
                    self.update_board(move[0], move[1], 2)
                    print("Player 2 played at [{}, {}]".format(move[0], move[1]))
                    print_board(self.board.board)
                    self.turn = 1

        result = self.board.game_result()
        print("Winner: Player {}".format(result))
        return result


if __name__ == '__main__':
    timestamp = time.time()
    filename = "training{}.json".format(timestamp)
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "lib", "ml", "training",
        filename)

    for _ in range(0, 20):
        sim = Simulator()
        result = sim.play_game()
        sim.store_game_result(result)
        sim.export_game_data(path)
