#!/usr/bin/client

import sys
import json
import socket
import random
import numpy as np

# from lib.montecarlo.game import GameState
from mctspy.tree.search import MonteCarloTreeSearch
from lib.montecarlo_derived.othello import OthelloGameState
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode


def get_move(player, board):
    board = np.array(board)

    initial_game_state = OthelloGameState(player, board)
    root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_game_state)
    mcts = MonteCarloTreeSearch(root)

    try:
        best_node = mcts.best_action(100)
        new_state = best_node.state
    except:
        print("GETTING RANDOM")
        random_move = random.choice(mcts.root.state.get_legal_actions())
        new_state = mcts.root.state.move(random_move)

    move = compare_states(initial_game_state, new_state)
    return [move.row, move.col]


def compare_states(old, new):
    valid_moves = old.get_legal_actions()

    for move in valid_moves:
        possible_state = old.move(move)
        if np.array_equal(possible_state.board, new.board):
            return move

    raise Exception("Invalid moves")


def prepare_response(move):
    response = '{}\n'.format(move).encode()
    print('sending {!r}'.format(response))
    return response


if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
    host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        while True:
            data = sock.recv(1024)
            if not data:
                print('connection to server closed')
                break
            json_data = json.loads(str(data.decode('UTF-8')))
            board = json_data['board']
            maxTurnTime = json_data['maxTurnTime']
            player = json_data['player']
            print(player, maxTurnTime, board)

            move = get_move(player, board)
            response = prepare_response(move)
            sock.sendall(response)
    finally:
        sock.close()
