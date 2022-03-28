import torch
import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
	def __init__(self, board_height, board_width):
		super().__init__()
		self.fc1 = nn.Linear(board_height*board_width, 100)
		self.fc2 = nn.Linear(100, 200)
		self.fc3 = nn.Linear(200, board_height*board_width)
	def forward(self, x):        
		x = self.fc1(x)
		x = F.relu(x)
		x = self.fc2(x)
		x = F.relu(x)
		x = self.fc3(x)
		return x