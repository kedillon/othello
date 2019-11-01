"""Functions to train and test the Othello model."""
import os
import glob
import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F

from lib.montecarlo.util import other_player
from lib.ml.othello_model import OthelloModel
from lib.ml.consumer import consume_json_training


# Run on GPU not CPU - uncomment this and add .to(DEVICE) to models when
# running remotely on the ml rig with NVIDIA graphics cards. When running
# locally, leave commented out and run with CPU. This is much slower, but
# CUDA is not enabled locally.
# DEVICE = "cuda"
NUM_FILTERS = 128
NUM_BLOCKS = 6
BATCH_SIZE = 300
LEARNING_RATE = 0.0003
WEIGHT_DECAY = 0.0001


def to_tensor(x):
    return torch.tensor(x).to(dtype=torch.float)  # Add DEVICE here when running remotely


def train(traning_batches, model_filename=None):
    # If we have a saved model, load the model
    if model_filename:
        model = load_model(model_filename, train=True)  # Add DEVICE here when running remotely
    else:
        model = OthelloModel(NUM_FILTERS, NUM_BLOCKS)  # Add DEVICE here when running remotely
        # Put this model in train mode
        model.train()

    optimizer = optim.AdamW(model.parameters(),
                            lr=LEARNING_RATE,
                            weight_decay=WEIGHT_DECAY)

    # 10 passes over the training data
    epoch = 0
    while epoch < 10:
        first = True
        for board, targets in traning_batches:
            x_input = to_tensor(board)
            y_value = to_tensor(targets[0])
            y_policy = to_tensor(targets[1])

            # Zero the gradients.
            # Pytorch accumulates these across batches by default, we don't want them
            optimizer.zero_grad()
            # Compute model output value and policy
            yhat_value, yhat_log_policy = model(x_input)
            # combine value and policy losses. use mean squared error for value prediction; use kl divergence
            # for policy prediction.
            # Compute loss for value and policy. Mean squared error for value
            # prediction, kl divergence for polidy prediction.
            # note: kl_div() expects log(predictions) but actual probabilities for targets
            loss1 = F.mse_loss(yhat_value, y_value)
            loss2 = F.kl_div(yhat_log_policy, y_policy, reduction='batchmean')
            loss = loss1 + loss2
            # Print the first batch so we can use it as testing-ish data.
            if first:
                print(loss)
                first = False
            # Compute gradients: partial derivatives of the loss
            # with respect to all model weights.
            loss.backward()
            # Nudge all weights in the direction of the gradient.
            optimizer.step()

        epoch += 1
        if epoch % 10 == 0:
            filename = "saved_othello_model.{}".format(epoch)
            torch.save(model.state_dict(), filename)
            print("saved %s" % filename)


def _evaluate(x_input, model):
    """
    Finds weights for a single batch of single batch of size 1.
    :param x_input: numpy array: shape (1,2,8,8)
    :return: tensor 1D length 1 [<expected value>], tensor 2D 1x64 [[<log probabilities>]]
    """
    x_input = to_tensor(x_input)

    # Compute model output value and policy
    yhat_value, yhat_log_policy = model(x_input)
    return yhat_value, yhat_log_policy


def evaluate_model_at_gamestate(gamestate, model):
    """
    Evaluates the model at a given GameState
    :param gamestate: GameState: represents the state of the game
    :return: int: value, list: policy
    """
    # Transform full board into 2 boards of 0s and 1s
    board = gamestate.board
    player1_board = np.array([
        [
            0 if val == 0 or val == 2 else 1
            for val in row
        ]
        for row in board
    ])
    player2_board = np.array([
        [
            0 if val == 0 or val == 1 else 1
            for val in row
        ]
        for row in board
    ])

    # Player is the player who created this state (NOT next)
    if other_player(gamestate.next_player) == 1:
        channels = [player1_board, player2_board]
    else:
        channels = [player2_board, player1_board]

    x_train = np.stack(channels).reshape(1, 2, 8, 8)

    value, policy = _evaluate(x_train, load_model(model))
    value_np = value.detach().numpy()  # value.cpu().detach().numpy() when running remotely
    policy_np = policy.detach().numpy()  # policy.cpu().detach().numpy() when running remotely

    return value_np[0], np.exp(policy_np.flatten().reshape(8, 8))


def load_model(filename, train=False):
    model = OthelloModel(NUM_FILTERS, NUM_BLOCKS)  # Add DEVICE here when running remotely

    filename = os.path.join(os.path.dirname(__file__), filename)
    model.load_state_dict(torch.load(filename, map_location="cpu"))  # Remove map_location="cpu" when running remotely.

    if train:
        model.train()
    else:
        model.eval()

    return model


def train_from_json(paths, model_filename):
    batches = []
    for path in paths:
        batches.extend(consume_json_training(path))

    train(batches, model_filename)


if __name__ == '__main__':

    all_training_files = glob.glob(os.path.join(os.path.dirname(__file__), "training", "*"))

    latest_train_files = sorted(
        all_training_files, key=os.path.getctime, reverse=True
    )[0:50]

    # Train the latest model (saved_othello_model.50) on training data
    train_from_json(latest_train_files, "saved_othello_model.50")
