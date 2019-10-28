#!/usr/bin/client

import sys
import json
import socket
import random
import numpy as np

from simulator.run import Player
from lib.montecarlo.tree import Tree
from lib.montecarlo.nodes import Node
from lib.montecarlo.game import GameState


# def get_move(player, board):
#
#     initial_game_state = GameState(player, board)
#     root = Node(state=initial_game_state)
#     mcts = Tree(root)
#
#     best_node, _ = mcts.best_move(300)
#     if best_node is None:
#         return None
#
#     move = best_node.transition_move
#     return [move.row, move.col]


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

        this_player = Player(None, "final_model")

        while True:
            data = sock.recv(1024)
            if not data:
                print('connection to server closed')
                break
            json_data = json.loads(str(data.decode('UTF-8')))
            board = json_data['board']
            maxTurnTime = json_data['maxTurnTime']
            player = json_data['player']

            if this_player.player_num is None:
                this_player.player_num = player

            print(player, maxTurnTime, board)

            board_state = GameState(player, board)

            move, _ = this_player.get_move(board_state)
            response = prepare_response(move)
            sock.sendall(response)
    finally:
        sock.close()
