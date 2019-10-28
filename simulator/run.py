import os
import json
import time

from simulator.util import print_board
from lib.montecarlo.util import other_player
from lib.montecarlo.game import GameState, Move
from simulator.player import RandomPlayer, MCTSPlayer, ModelPlayer


class Simulator:
    def __init__(self, player1_type, player2_type):
        """
        Initialize the game simulator.
        :param player1_type: string: name of this player's ml model, "random",
               or mcts to use vanilla mcts
        :param player2_type: string: name of this player's ml model, "random",
               or mcts to use vanilla mcts
        """
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
        if player1_type == "random":
            self.p1 = RandomPlayer(1)
        elif player1_type == "mcts":
            self.p1 = MCTSPlayer(1)
        else:
            self.p1 = ModelPlayer(1, player1_type)

        if player2_type == "random":
            self.p2 = RandomPlayer(2)
        elif player2_type == "mcts":
            self.p2 = MCTSPlayer(2)
        else:
            self.p2 = ModelPlayer(2, player2_type)

        self.turn = 1

        # All game states accessed during the game.
        self.all_game_states = []

    def update_board(self, row, col, player):
        """
        Make a move chosen by a player and update self.board.
        :param row: int: row chosen by player
        :param col: int: column chosen by player
        :param player: int: player who made the move.
        """
        move = Move(row, col, player)
        self.board = self.board.move(move)

    def store_game_state(self, counts):
        """
        Adds a single game state to the list of game states for this game.
        :param counts: list: number of times each square was visited by mcts
        """
        if not counts:
            print("Cannot store training data with invalid y_policy")
            return
        self.all_game_states.append([self.board, counts])

    def store_game_result(self, result):
        """
        Adds the result to each training example for this game.
        :param result: int: win/loss value for the game.
        """
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
        """
        Appends game data to a json file.
        :param path: string: path to json file.
        """
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

    def play_game(self, debug=False, train=False):
        """
        Play a game using the simulator. Players take turns, self.board updates.
        :param debug: bool: when debug flag is True, every game state prints.
        :return: int, 2D list. Game result, final board state.
        """
        while not self.board.game_over():
            if self.turn == 1:
                move, all_move_visits = self.p1.get_move(self.board)

                if move is None:
                    self.update_board(None, None, 1)
                    if debug:
                        print("Player 1 has no valid moves.")
                    self.turn = 2
                else:
                    if train:
                        # Save current state for training
                        self.store_game_state(all_move_visits)
                    self.update_board(move[0], move[1], 1)
                    if debug:
                        print("Player 1 played at [{}, {}]".format(move[0], move[1]))
                        print_board(self.board.board)
                    self.turn = 2
            else:
                move, all_move_visits = self.p2.get_move(self.board)

                if move is None:
                    self.update_board(None, None, 2)
                    if debug:
                        print("Player 2 has no valid moves.")
                    self.turn = 1
                else:
                    if train:
                        # Save current state for training
                        self.store_game_state(all_move_visits)
                    self.update_board(move[0], move[1], 2)
                    if debug:
                        print("Player 2 played at [{}, {}]".format(move[0], move[1]))
                        print_board(self.board.board)
                    self.turn = 1

        print_board(self.board.board)
        result = self.board.game_result()
        return result, self.board.board


def run_create_training_data(player1_type, player2_type):
    """
    Play 20 games and write training data to a json file in lib/ml/training/
    :param player1_type: string: name of this player's ml model, "random",
           or None to use vanilla mcts
    :param player2_type: string: name of this player's ml model, "random",
           or None to use vanilla mcts
    :return:
    """
    timestamp = time.time()
    filename = "training{}.json".format(timestamp)
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "lib", "ml", "training",
        filename)

    for _ in range(0,20):
        sim = Simulator(player1_type=player1_type, player2_type=player2_type)
        result, _ = sim.play_game(train=True)

        sim.store_game_result(result)
        sim.export_game_data(path)


def run_single_game(player1_type, player2_type):
    """
    Runs a single game and prints game output to stdout.
    :param player1_type: string: name of this player's ml model, "random",
           or None to use vanilla mcts
    :param player2_type: string: name of this player's ml model, "random",
           or None to use vanilla mcts
    """
    sim = Simulator(player1_type=player1_type, player2_type=player2_type)
    result, final_board = sim.play_game(debug=True)
    print("Winner: Player {}".format(result))
    print_board(final_board)


# Run the simulator using specified player types.
if __name__ == '__main__':
    p1_type = "random"      # Random player
    p2_type = "mcts_short"  # Use mcts_short model

    # To generate training data, uncomment the following line.
    # run_create_training_data(player1_type, player2_type)

    # To play a single game using the simulator, uncomment the following line.
    run_single_game(p1_type, p2_type)

