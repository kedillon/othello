"""Functions to train and test the Othello model."""
import os
import torch
import torch.optim as optim
import torch.nn.functional as F

from lib.ml.othello_model import OthelloModel
from lib.ml.consumer import consume_json_training


# Run on GPU not CPU
# DEVICE = "cuda"
NUM_FILTERS = 128
NUM_BLOCKS = 6
BATCH_SIZE = 300
LEARNING_RATE = 0.0003
WEIGHT_DECAY = 0.0001


def to_tensor(x):
    return torch.tensor(x).to(dtype=torch.float)


def train(traning_batches, model_filename=None):
    model = OthelloModel(NUM_FILTERS, NUM_BLOCKS)

    # If we have a saved model, load the model

    model.train()
    optimizer = optim.AdamW(model.parameters(),
                            lr=LEARNING_RATE,
                            weight_decay=WEIGHT_DECAY)

    # 50 passes over the training data
    epoch = 0
    while epoch < 50:
        first = True  # just gonna treat the first batch as test & won't train on it.
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
            loss = F.mse_loss(yhat_value, y_value) + F.kl_div(yhat_log_policy, y_policy, reduction='batchmean')
            if first:
                print(loss)
                first = False
            else:
                # Compute gradients: partial derivatives of the loss
                # with respect to all model weights.
                loss.backward()
                # Nudge all weights in the direction of the gradient.
                optimizer.step()

        epoch += 1
        if epoch % 10 == 0:
            filename = f"saved_othello_model.{epoch}"
            torch.save(model.state_dict(), filename)
            print("saved %s" % filename)


def evaluate(batch):
    """
    Finds weights for a single batch of single batch of size 1.
    :param batch:
    :return:
    """
    model = OthelloModel(NUM_FILTERS, NUM_BLOCKS)
    model.load_state_dict(torch.load("saved_othello_model.50"))
    model.eval()

    for board, targets in batch:
        x_input = to_tensor(board)
        y_value = to_tensor(targets[0])
        y_policy = to_tensor(targets[1])

        # Compute model output value and policy
        yhat_value, yhat_log_policy = model(x_input)
        return yhat_value, yhat_log_policy


if __name__ == '__main__':
    training_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "training.json")
    batches = consume_json_training(training_path)

    # train(batches)
