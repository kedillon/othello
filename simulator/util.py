"""Utility functions for the Othello simulator."""


def format_row(row, idx):
    return str(idx) + ' ||  ' + '  |  '.join(" " if x == 0 else str(x) for x in row) + '  |'


def print_board(board):
    line = "\n    ================================================\n"
    cols = ["0", "1", "2", "3", "4", "5", "6", "7"]

    print("      " +
          ("     ".join(cols)) +
          line +
          (line.join(format_row(row, idx) for idx, row in enumerate(board))) +
          line)
