"""Othello neural network."""
import torch
import torch.nn as nn
import torch.nn.functional as F

from lib.ml.residual_block import ResidualBlock


class OthelloModel(nn.Module):
    def __init__(self, num_filters, num_blocks):
        super(OthelloModel, self).__init__()
        # Two in_channels, one for player 1, one for player 2.
        # The one on top is the player that created this state.
        # Turns our 8x8 input channels into num_filters 8x8 filters.
        self.initial_conv = nn.Conv2d(in_channels=2,
                                      out_channels=num_filters,
                                      kernel_size=3,
                                      padding=1)
        # ModuleList of ResidualBlocks
        self.residual_blocks = nn.ModuleList(
            [ResidualBlock(num_filters) for _ in range(num_blocks)])
        # Policy conv turns out num_filters channels into the single
        # channel 8x8 output with weights for each move
        self.policy_conv = nn.Conv2d(in_channels=num_filters,
                                     out_channels=1,
                                     kernel_size=1)
        # Fully connected layers produce value prediction (chance of win/loss)
        # from our num_filters channels. Converges to 40 features, then 20, then 1
        self.fc1 = nn.Linear(num_filters * 8 * 8, 40)
        self.fc2 = nn.Linear(40, 20)
        self.fc3 = nn.Linear(20, 1)

    def forward(self, x):
        # Initial convolution and transformations using residual blocks
        x = self.initial_conv(x)
        for block in self.residual_blocks:
            x = block(x)

        # Perform policy convolution to get weights for each move
        policy_output = self.policy_conv(x)
        # Flatten from 4D tensor (BATCH_SIZE * 1 * 8 * 8)
        # to 2D tensor (BATCH_SIZE * 64)
        flattened = torch.flatten(policy_output, start_dim=1)
        # Extract log(policy probability distribution)
        # This will be an input to loss function.
        # To use to predict probs, must exponentiate
        policy = F.log_softmax(flattened, dim=1)

        # Run fully connected layers with dropout to produce value prediction.
        # Dropout will sample a subset of neurons to use and drop connections
        # so we arent't overfitting. Can't rely exclusively on one set of weights.
        # http://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf
        value = self.fc1(torch.flatten(x, start_dim=1))
        value = F.dropout(F.relu(value), 0.5)
        value = self.fc2(value)
        value = F.dropout(F.relu(value), 0.5)
        value = self.fc3(value)
        value = torch.flatten((torch.tanh(value) + 1) / 2)

        return value, policy
