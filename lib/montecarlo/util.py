def in_bounds(row, col):
    """
    Check that location is within an Othello board.
    :param location: list: Represents a location. Form: [row, col]
    :return: bool
    """
    if row < 0 or row > 7 or col < 0 or col > 7:
        return False
    return True


def other_player(player):
    if player == 1:
        return 2
    else:
        return 1


def increment_row_col(row, col, direction):
    """
    Increments/decrements row and col based on search direction
    :param row: int: Represents the row
    :param col: int: Represents the col
    :param direction: string: Represents direction of search.
                              One of: ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]
    :return: int, int: new row and column
    """
    if direction == "N":
        return row - 1, col
    if direction == "S":
        return row + 1, col
    if direction == "E":
        return row, col + 1
    if direction == "W":
        return row, col - 1
    if direction == "NE":
        return row - 1, col + 1
    if direction == "NW":
        return row - 1, col - 1
    if direction == "SE":
        return row + 1, col + 1
    if direction == "SW":
        return row + 1, col - 1
    else:
        return None
