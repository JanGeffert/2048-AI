import copy
import numpy as np

class Board():

	def __init__(self, size=4, config=None):

		self.size = size
		self.prob2 = .9
		self.prob4 = 1 - self.prob2

		self.LEFT = "LEFT"
		self.RIGHT = "RIGHT"
		self.UP = "UP"
		self.DOWN = "DOWN"

		self.grid = [[0] * x for x in [size] * size ]
		self.score = 0

		if config is not None:
			# self.grid = config
		else:
			# Initialize random grid with either 1, 2 or 3 blocks
			numberStart = np.random.randint(1, 4)
			self.placeRandomTile(numberStart)

	def __str__(self):
		totString = ""
		for i in range(self.size):
			rowString = "|"
			for j in range(self.size):
				rowString += str(self.grid[i][j]) + "|"
			totString += rowString + "\n"
		return totString

	def copy(self):
		return copy.deepcopy(self)

	def initBoard(self):
		self.grid = [[0] * x for x in [self.size] * self.size ]
		self.score = 0

		numberStart = np.random.randint(1, 4)
		self.placeRandomTile(numberStart)

	def emptySquares(self):
		"""
		Return a list of coordinates tuples of empty squares.
		"""
		res = []
		for i in range(self.size):
			for j in range(self.size):
				if self.grid[i][j] == 0:
					res.append((i, j))
		return res

	def validMoves(self):
		"""
		Return a list of valid moves.
		"""
		moves = set([])
		
		for i in range(self.size):
			for j in range(self.size):
				# Check if Left is valid
				if j >= 1:
					if (self.grid[i][j] == self.grid[i][j-1] and self.grid[i][j] != 0) or \
					   (self.grid[i][j] > 0 and self.grid[i][j-1] == 0):
				   		moves.add(self.LEFT)
				# Check if Right is valid
				if j <= self.size - 2:
					if (self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] != 0) or \
				   	   (self.grid[i][j] > 0 and self.grid[i][j+1] == 0):
				   		moves.add(self.RIGHT)
				# Check if Up is valid
				if i >= 1:
					if (self.grid[i][j] == self.grid[i-1][j] and self.grid[i][j] != 0) or \
				   	   (self.grid[i][j] > 0 and self.grid[i-1][j] == 0):
				   		moves.add(self.UP)
				# Check if Down is valid
				if i < self.size - 1:
					if (self.grid[i][j] == self.grid[i+1][j] and self.grid[i][j] != 0) or \
				   	   (self.grid[i][j] > 0 and self.grid[i+1][j] == 0):
				   		moves.add(self.DOWN)

		return list(moves)

	def shift(self, move):
		"""
		Shift all tiles in the board according to move.
		Note that this does *not* generate a random block after shifting.
		The latter is implemented in placeRandomTile.
		"""

		if move == self.LEFT:
			for i in range(self.size):
				# move each row to the left
				self.grid[i], newVal = self.moveLeft(self.grid[i])
				self.score += newVal

		elif move == self.RIGHT:
			for i in range(self.size):
				# move each row to the right
				self.grid[i], newVal = self.moveRight(self.grid[i])
				self.score += newVal

		elif move == self.DOWN:
			for j in range(self.size):
				col, newVal = self.moveDown([row[j] for row in self.grid])
				self.score += newVal
				for i, row in enumerate(self.grid):
					row[j] = col[i]

		elif move == self.UP:
			for j in range(self.size):
				col, newVal = self.moveUp([row[j] for row in self.grid])
				self.score += newVal
				for i, row in enumerate(self.grid):
					row[j] = col[i]  

		else:
			raise ValueError("Invalid move: Only UP, LEFT, BOTTOM, RIGHT \
				are permitted.")

	def updateBoard(self, move, printOpts=True):
		if move in self.validMoves():
			self.shift(move)
			self.placeRandomTile(1)
		if printOpts:
			print(self, "Score: {}".format(self.score))

	def moveLeft(self, row):
		newValue = 0
		for i, block in enumerate(row):
			if block != 0 and i > 0:
				# Move left until hits a block
				temp = i
				while temp > 0:
					if row[temp - 1] == 0:
						row[temp - 1] = block
						row[temp] = 0
					elif row[temp - 1] == block:
						row[temp - 1] = 2 * block
						row[temp] = 0
						newValue += 2 * block
						break
					else:
						break
					temp -= 1
		return row, newValue

	def moveRight(self, row):
		newValue = 0
		for i, block in reversed(list(enumerate(row))):
			if block != 0 and i < self.size - 1:
				# Move right until hits a block
				temp = i
				while temp < self.size - 1:
					if row[temp + 1] == 0:
						row[temp + 1] = block
						row[temp] = 0
					elif row[temp + 1] == block:
						row[temp + 1] = 2 * block
						row[temp] = 0
						newValue += 2 * block
						break
					else:
						break
					temp += 1
		return row, newValue

	def moveDown(self, col):
		newValue = 0
		for i, block in reversed(list(enumerate(col))):
			if block != 0 and i < self.size - 1:
				# Move down until hits a block or border
				temp = i
				while temp < self.size - 1:
					if col[temp + 1] == 0:
						col[temp + 1] = block
						col[temp] = 0
					elif col[temp + 1] == block:
						col[temp + 1] = 2 * block
						col[temp] = 0
						newValue += 2 * block
						break
					else:
						break
					temp += 1
		return col, newValue

	def moveUp(self, col):
		newValue = 0
		for i, block in enumerate(col):
			if block != 0 and i > 0:
				# Move up until hits a block or border
				temp = i
				while temp > 0:
					if col[temp - 1] == 0:
						col[temp - 1] = block
						col[temp] = 0
					elif col[temp - 1] == block:
						col[temp - 1] = 2 * block
						col[temp] = 0
						newValue += 2 * block
						break
					else:
						break
					temp -= 1
		return col, newValue

	def placeRandomTile(self, num):
		"""
		Add num new tiles to random empty squares of the board.
		"""

		emptySquares = self.emptySquares()
		locations = np.random.choice(range(len(emptySquares)),
									size=num, replace=False)
		for k in locations:
			i, j = emptySquares[k]
			choice = np.random.random()
			if choice > 1 - self.prob2:
				self.grid[i][j] = 2
			else:
				self.grid[i][j] = 4

	def isGameOver(self):
		"""
		Return True if the game is over, False otherwise.
		"""

		moves = self.validMoves()
		if len(moves) == 0:
			return True
		else:
			return False

	def maxTile(self):
		"""
		Return the value of the tile with the highest value.
		"""

		# iterate over all tiles in the board
		maxT = 0
		for i in range(self.size):
			for j in range(self.size):
				val = self.grid[i][j]
				if val > maxT:
					maxT = val
		return maxT

	def numberEmpty(self):
		"""
		Return the number of empty squares.
		"""

		# iterate over each square of the board, counting occurences of 0
		return len(self.emptySquares())

	def placeTile(self, i, j, val):
		"""
		Place a tile with a given value at position i,j on the board.
		"""

		# ensure proper usage
		if self.grid[i][j] != 0:
			raise ValueError("Tried to place a tile in a non-empty square.")

		if i >= self.size or j >= self.size:
			raise ValueError("Invalid tile position.")

		# place the new tile in the grid
		self.grid[i][j] = val

	def getSuccessors(self, move):
		"""Return the possible successor states and their associated
		probabilities in a list of tuples.
		"""

		# make sure that the move is valid
		if move not in self.validMoves():
			return []

		pass

	def allPossibleNextStates(self):
		original_board = self.copy()
		possible_next_states = []

		for move in self.validMoves():
			shift_board = original_board.copy()
			shift_board.shift(move)
			num_empty = shift_board.numberEmpty()

			for i in range(shift_board.size):
				for j in range(shift_board.size):
					if shift_board.grid[i][j] == 0:
						board2 = shift_board.copy()
						board2.placeTile(i, j, 2)
						b2prob = (1 / num_empty) * board2.prob2
					
						board4 = shift_board.copy()
						board4.placeTile(i, j, 4)
						b4prob = (1 / num_empty) * board4.prob4

						possible_next_states.append((board2, b2prob))
						possible_next_states.append((board4, b4prob))

		return possible_next_states

		# futureBoards = []
		# numEmpty = self.numberEmpty()
		# for i in range(self.size):
		# 	for j in range(self.size):
		# 		if self.grid[i][j] == 0:
		# 			board2 = self.copy()
		# 			board4 = self.copy()

		# 			board2.placeTile(i, j, 2)
		# 			b2prob = 1 / numEmpty * self.prob2

		# 			board4.placeTile(i, j, 4)
		# 			b4prob = 1 / numEmpty * self.prob4

		# 			futureBoards.append((board2, b2prob))
		# 			futureBoards.append((board4, b4prob))
		# return futureBoards
