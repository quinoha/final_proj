import torch
from torch import nn
import numpy as np

class workout_mlp(nn.Module):
    def __init__(self, in_dim, out_dim, scaling_list, out_act='sigmoid', batchnorm=0):
        super().__init__()

        layers = []
        current_in_dim = in_dim


        # ============================ stack hidden layers ============================
        for scale in scaling_list:
            h_size = int(in_dim * scale)

            layers.append(nn.Linear())
            layers.append(nn.Tanh)

            if batchnorm:
                layers.append(nn.BatchNorm1d(h_size))

            current_in_dim = h_size
        
        # ============================ Output layers ============================
        layers.append(nn.Linear())

        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)