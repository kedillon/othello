from lib.montecarlo.game import GameState, Move


def test_move_is_legal():
    board_state = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    game_state = GameState(1, board_state)

    move1 = Move(1, 1, 1)  # Not valid, not connected to anything
    move2 = Move(1, 3, 1)  # Not valid, adjacent to other player but does not flip tiles
    move3 = Move(3, 5, 1)  # Valid, flips one in two directions
    move4 = Move(4, 6, 1)  # Valid, flips more than one in one direction
    move5 = Move(6, 3, 1)  # Not valid, adjacent to this player, doesn't flip
    move6 = Move(4, 4, 1)  # Not valid, square isn't empty
    move7 = Move(8, 5, 1)  # Not valid, out of bounds
    move8 = Move(3, 8, 1)  # Not valid, out of bounds

    assert not game_state.move_is_legal(move1)
    assert not game_state.move_is_legal(move2)
    assert game_state.move_is_legal(move3)
    assert game_state.move_is_legal(move4)
    assert not game_state.move_is_legal(move5)
    assert not game_state.move_is_legal(move6)
    assert not game_state.move_is_legal(move7)
    assert not game_state.move_is_legal(move8)

    game_state = GameState(2, board_state)

    move9 = Move(1, 3, 2)  # Not valid, adjacent to this player, doesn't flip
    move10 = Move(6, 3, 2)  # Not valid, adjacent to other player but does not flip tiles
    move11 = Move(6, 2, 2)  # Valid, flips diagonally
    move12 = Move(2, 2, 2)  # Valid, flips diagonally
    move13 = Move(4, 2, 2)  # Valid, flips diagonally

    assert not game_state.move_is_legal(move9)
    assert not game_state.move_is_legal(move10)
    assert game_state.move_is_legal(move11)
    assert game_state.move_is_legal(move12)
    assert game_state.move_is_legal(move13)


def test_get_legal_moves():
    board_state = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 1, 2, 0, 0, 0],
        [0, 0, 0, 1, 2, 2, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    game_state = GameState(1, board_state)

    correct = [
        Move(3, 5, 1),
        Move(4, 6, 1),
        Move(1, 5, 1),
        Move(2, 5, 1),
        Move(5, 5, 1)
    ]

    legal_moves = game_state.get_legal_moves(1)

    assert len(legal_moves) == len(correct)
    for move in correct:
        assert str(move) in [str(legalmove) for legalmove in legal_moves]
