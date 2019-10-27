"""
Othello residual block component.

Residual blocks allow us to skip training multiple
layers because we can directly learn an identity function.
We can train deeper networks with more layers. Training error stays down.
Skip connection gives you a landscape with different scales.
Earlier in the network = bigger, later = smaller. We can train gradient deeper in the network faster.
https://towardsdatascience.com/residual-blocks-building-blocks-of-resnet-fd90ca15d6ec
"""
import torch.nn as nn
import torch.nn.functional as F


class ResidualBlock(nn.Module):
    def __init__(self, num_filters):
        super(ResidualBlock, self).__init__()
        # Layers that use kernals to recognize features and patterns in the data
        self.conv1 = nn.Conv2d(num_filters, num_filters, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(num_filters, num_filters, kernel_size=3, padding=1)
        # Batch normalization layers. Allows each layer to learn by itself
        # more independently of other layers.
        # https://towardsdatascience.com/batch-normalization-in-neural-networks-1ac91516821c)
        self.norm1 = nn.BatchNorm2d(num_filters)
        self.norm2 = nn.BatchNorm2d(num_filters)

    def forward(self, x):
        residual = x
        # Conv, normalize, activate.
        x = self.conv1(x)
        x = self.norm1(x)
        x = F.relu(x)
        # Conv, normalize, add residual back, activate.
        x = self.conv2(x)
        x = self.norm2(x)
        x += residual
        return F.relu(x)
