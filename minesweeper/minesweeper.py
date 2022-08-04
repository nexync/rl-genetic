import random
import numpy as np
import collections

class Minesweeper():
	def __init__(self, board_length = 8, board_width = 8, num_mines = 10, mine_indicator = 9):
		self.board_length = board_length
		self.board_width = board_width
		self.initial_mines = num_mines
		self.num_mines = num_mines
		self.mine_indicator = mine_indicator
		self.remaining_squares = board_length*board_width
		self.episode = 0
		self.environment = self.generate_environment(board_length, board_width, num_mines, mine_indicator)

	def generate_environment(self,board_length, board_width, num_mines, mine_indicator):
			'''
				Parameters:
					board_length: length of desired board
					board_width: width of desired board
				Returns:
					board: board_length * board_width * 2 array 
					       first coordinate represents hidden/reveal (0/1) second 
					       second coordinate represents mine/# mine neighbors (-1/n)

			'''
			board = [[[0] * 2 for _ in range(board_width)] for _ in range(board_length)]
			traversal = list(range(board_length*board_width))
			random.shuffle(traversal)
			mines = num_mines 

			for k, square in enumerate(traversal):
				
				x = square//board_width
				y = square%board_width
				if random.random() < mines/(board_width*board_length - k):
					board[x][y][1] = mine_indicator
					mines -= 1

					addendums = [[0]*3 for _ in range(3)]
					if x > 0:
						for k in range(3):
							addendums[0][k] += 1 
					if y > 0:
						for k in range(3):
							addendums[k][0] += 1
					if x < board_length-1:
						for k in range(3):
							addendums[2][k] += 1
					if y < board_width-1:
						for k in range(3):
							addendums[k][2] += 1

					for j in range(3):
						for k in range(3):
							if j % 2 == 0 and k % 2 == 0 and addendums[j][k] == 2:
								if board[x + (j-1)][y + (k-1)][1] != mine_indicator:	board[x + (j-1)][y + (k-1)][1] += 1
							elif j % 2 == 1 and k % 2 == 1:
								continue
							elif (j % 2 == 1 or k % 2 == 1) and addendums[j][k] == 1:
								if board[x + (j-1)][y + (k-1)][1] != mine_indicator:	board[x + (j-1)][y + (k-1)][1] += 1
			return board

	def print_board(self, info):
		if info == "all":
			for row in self.environment:
				for sq in row:
					print(sq[1], end = " ")
				print(" ", end = '\n')
		else:
			board = self.return_board_state()
			for row in board:
				for sq in row:
					print(sq, end = " ")
				print(" ", end = '\n')

	def return_board_state(self):
		state = [[0] * self.board_width for _ in range(self.board_length)]
		for j in range(self.board_length):
			for k in range(self.board_width):
				if self.environment[j][k][0] == 0:
					state[j][k] = -1
				else:
					state[j][k] = self.environment[j][k][1]
		return state

	
	def reveal_square(self, square):
		if self.environment[square[0]][square[1]][1]:
			return (-0.33, False)
		directions = [(1,0), (-1,0), (0,1), (0,-1)]
		seen = set()
		qu = collections.deque()
		seen.add((square//self.board_width, square%self.board_width))
		qu.append((square//self.board_width, square%self.board_width))
		while len(qu) > 0:
			sq = qu.popleft()
			if sq[0] >= 0 and sq[0] < self.board_length and sq[1] >= 0 and sq[1] < self.board_width:
				if self.environment[sq[0]][sq[1]][1] == self.mine_indicator:
					return (-1, True)
				if self.environment[sq[0]][sq[1]][0] == 0 and self.environment[sq[0]][sq[1]][1] != self.mine_indicator:
					self.environment[sq[0]][sq[1]][0] = 1
					self.remaining_squares -= 1
					if self.remaining_squares == self.num_mines:
						return (10, True) #here you win
					if self.environment[sq[0]][sq[1]][1] == 0:
						for d in directions:
							newx = sq[0] + d[0]
							newy = sq[1] + d[1]
							if (newx, newy) not in seen:
								seen.add((newx,newy))
								qu.append((newx,newy))
		return (1, False) #here progress

	def step(self, action):
		reward, has_ended = self.reveal_square(action)
		curr_environment = self.return_board_state()
		return (curr_environment, reward, has_ended, {})


	def sample_random_action(self):
		k = list(range(self.board_length*self.board_width))
		return k[0]

	def reset(self):
		self.num_mines = self.initial_mines
		self.remaining_squares = self.board_length*self.board_width
		self.environment = self.generate_environment(self.board_length, self.board_width, self.num_mines, self.mine_indicator)
