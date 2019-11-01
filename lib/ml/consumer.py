"""Consumes training data from json."""
import json
import numpy as np

BATCH_SIZE = 300


def consume_json_training(path):
    """
    Consumes training data from a json file.
    :param path: string: path to json file.
    :return: array of batches: each batch is a multi-dimensional numpy array
             to be used for training
    """
    with open(path) as infile:
        data = json.load(infile)

        batches = []

        i = 0
        # Add to batches while there is more data
        while i + BATCH_SIZE < len(data):
            x_train = []
            y_values = []
            y_policies = []

            # Create a batch
            for example in data[i:(i + BATCH_SIZE)]:
                player = example["created_by"]
                full_board = example["board"]
                move_visits = example["move_visits"]
                winloss = example["winloss"]

                # Transform full board into 2 boards of 0s and 1s
                player1_board = np.array([
                    [
                        0 if val == 0 or val == 2 else 1
                        for val in row
                    ]
                    for row in full_board
                ])
                player2_board = np.array([
                    [
                        0 if val == 0 or val == 1 else 1
                        for val in row
                    ]
                    for row in full_board
                ])

                if player == 1:
                    channels = [player1_board, player2_board]
                else:
                    channels = [player2_board, player1_board]

                board_3d = np.stack(channels)

                x_train.append(board_3d)
                y_values.append(winloss)
                y_policies.append(np.array(move_visits))

            # Stack inputs, winloss, and policies.
            # Combine into tuple, append to batches
            batches.append(
                (
                    np.stack(x_train),
                    (np.stack(y_values), np.stack(y_policies))
                )
            )
            i += BATCH_SIZE

        return batches
