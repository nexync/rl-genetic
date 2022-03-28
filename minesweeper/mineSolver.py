import minesweeper as m
import dqn

class MinesweeperSolver():
	def __init__(self):
		self.mine_environment = m.Minesweeper()
		self.dqn = dqn.DQN()