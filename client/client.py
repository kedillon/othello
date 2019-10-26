#!/usr/bin/client

import sys
import json
import socket

from random import randint
from lib.montecarlo.game import GameState


def get_move(player, board):
    # TODO determine valid moves
    # TODO determine best move

    game_state = GameState(player, board)
    legal_moves = game_state.get_legal_moves(player)

    idx = randint(0, len(legal_moves) - 1)

    try:
        chosen = legal_moves[idx]
    except:
        print(f"INDEX: {idx}, NUM_LEGAL: {len(legal_moves)}")

    return [chosen.row, chosen.col]


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
