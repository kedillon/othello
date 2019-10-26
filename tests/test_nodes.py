from lib.montecarlo.nodes import Node
from lib.montecarlo.game import GameState, Move


def test_get_untried():
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
    initial_state = GameState(1, initial_board)
    root = Node(initial_state)

    untried = root.get_untried_moves()

    correct = [
        Move(5, 3, 1),
        Move(4, 2, 1),
        Move(2, 4, 1),
        Move(3, 5, 1),
    ]

    assert len(untried) == len(correct)
    for elem in untried:
        assert elem in correct
        assert elem in root.untried_moves

    root.untried_moves.pop()

    assert len(root.untried_moves) == len(correct) - 1
    assert len(root.get_untried_moves()) == len(correct) - 1


def test_backprop():
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
    initial_state = GameState(1, initial_board)
    root = Node(initial_state)

    # First move
    move = Move(5, 3, root.state.next_player)
    state_1 = root.state.move(move)
    n1 = Node(state_1, parent=root, transition_move=move)

    # Second move
    move = Move(5, 2, n1.state.next_player)
    state_2 = n1.state.move(move)
    n2 = Node(state_2, parent=n1, transition_move=move)

    result = 2
    print(n2)
    n2.backpropagate(2)

    print(f"N1 visits: {n1.visit_count}, N1 wins: {n1.win_score}")
    print(f"N2 visits: {n2.visit_count}, N2 wins: {n2.win_score}")
