import random
import numpy as np

class Minesweeper:
	def __init__(self, board_length = 8, board_width = 8, num_mines = 10):
		self.board_length = board_length
		self.board_width = board_width
		self.board = generate(board_length, board_width)
		self.mines = num_mines
		
		def generate(board_length, board_width, num_mines):
			'''
				Parameters:
					board_length: length of desired board
					board_width: width of desired board
				Returns:
					board: board_length * board_width * 2 array 
					       first coordinate represents hidden/reveal (0/1) second 
					       second coordinate represents mine/# mine neighbors (-1/n)

			'''
			board = [[[0] * 2 for _ in range(board_length)] for _ in range(board_width)]
			traversal = list(range(board_length*board_width))
			random.shuffle(traversal)
			mines = num_mines 

			for k, square in enumerate(traversal):
				x = square//board_length
				y = square%board_width
				if random.random() < mines/(board_width*board_length - k):
					board[x][y][1] = -1
					mines -= 1
					if x > 0:
						if board[x-1][y] != -1:
							board[x-1][y] += 1
					if y > 0: 
						if board[x][y-1] != -1:
							board[x][y-1] += 1
					if x < board_length - 1:
						if board[x+1][y] != -1:
							board[x+1][y] += 1
					if y < board_width - 1:
						if board[x][y+1] != -1:
							board[x][y+1] += 1
			return board
	
