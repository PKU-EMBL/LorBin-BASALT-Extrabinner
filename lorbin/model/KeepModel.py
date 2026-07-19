import torch.nn as nn



class KeepModel(nn.Module):
    def __init__(self, input_size):
        super(KeepModel, self).__init__()
        self.linear1 = nn.Linear(input_size,input_size)
        self.relu = nn.LeakyReLU()
        self.linear2 = nn.Linear(input_size,1)
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        x = self.relu(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        return x


