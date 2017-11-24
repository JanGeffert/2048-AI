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
			self.grid = copy.deepcopy(config)
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

		def shiftRow(vals):
			"""
			Shift values within a row to the left.  Will move a value to 
			the left until it hits another block.  If that block
			has the same value, then the value is doubled.  Otherwise we 
			stop shifting the value left.
			"""
			newValue = 0
			possibleMerge = [True] * len(vals)
			for i in range(1, len(vals)):
				val = vals[i]
				if val != 0:
					# Move left until hits a block
					temp = i
					while temp > 0:
						# Moves left because empty
						if vals[temp - 1] == 0:
							vals[temp - 1] = val
							vals[temp] = 0
						# Moves left for merge
						elif vals[temp - 1] == val:
							# check if mergeable
							if possibleMerge[temp - 1]:
								vals[temp - 1] = 2 * val
								vals[temp] = 0
								newValue += 2 * val
								possibleMerge[temp - 1] = False
								break
							else:
								break
						else:
							break
						temp -= 1
			return vals, newValue

		if move == self.LEFT:
			for i in range(self.size):
				# move each row to the left
				self.grid[i], newVal = shiftRow(self.grid[i])
				self.score += newVal

		elif move == self.RIGHT:
			for i in range(self.size):
				# move each row to the right
				row = list(reversed(self.grid[i]))
				revRow, newVal = shiftRow(row)
				self.grid[i] = list(reversed(revRow))
				self.score += newVal

		elif move == self.DOWN:
			for j in range(self.size):
				col = list(reversed([row[j] for row in self.grid]))
				col, newVal = shiftRow(col)
				col = list(reversed(col))
				self.score += newVal
				for i, row in enumerate(self.grid):
					row[j] = col[i]

		elif move == self.UP:
			for j in range(self.size):
				col = [row[j] for row in self.grid]
				col, newVal = shiftRow(col)
				self.score += newVal
				for i, row in enumerate(self.grid):
					row[j] = col[i]  

		else:
			raise ValueError("Invalid move: Only UP, LEFT, BOTTOM, RIGHT \
are permitted.")

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

	def maxTilePosition(self):
		"""
		Return position of maxTile.
		"""
		maxT = 0
		bestI = None
		bestJ = None
		for i in range(self.size):
			for j in range(self.size):
				val = self.grid[i][j]
				if val > maxT:
					maxT = val
					bestI = i
					bestJ = j
		return (bestI, bestJ)

	def getNeighbors(self, pos):
		"""
		Returns the neighbor locations of any given tile location.
		"""
		possibleX = []
		possibleY = []
		x, y = pos

		if x > 0 and x < self.size - 1:
			possibleX = [x-1, x, x + 1]
		elif x > 0:
			possibleX = [x-1, x]
		else:
			possibleX = [x, x + 1]

		if y > 0 and y < self.size - 1:
			possibleY = [y-1, y, y + 1]
		elif y > 0:
			possibleY = [y-1, y]
		else:
			possibleY = [y, y + 1]

		neighbors = [(i, j) for (i, j) in zip(possibleX, possibleY)]
		return neighbors

	def tileDiff(self):
		"""
		Returns the total difference between the values of 
		neighboring tiles.
		"""
		diff = 0
		for i in range(self.size):
			for j in range(self.size):
				neighbors = self.getNeighbors((i,j))
				for x, y in neighbors:
					diff += np.abs(self.grid[x][y] - self.grid[i][j])
		return diff

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

	def getSuccessor(self, move, printOpts=True):
		"""
		Return a random successor board.
		"""
		successor = self.copy()
		if move in successor.validMoves():
			successor.shift(move)
			successor.placeRandomTile(1)
		if printOpts:
			print(successor, "Score: {}".format(successor.score))
		return successor


	def getAllSuccessors(self, move):
		"""
		Return the possible successor states and their associated
		probabilities in a list of tuples.
		"""

		statesList = []
		probsList = []

		# make sure that the move is valid
		if move not in self.validMoves():
			return []

		duplicate = self.copy()

		duplicate.shift(move)

		emptyIndices = duplicate.emptySquares()
		numEmptyInd = len(emptyIndices)
		for empty in emptyIndices:
			child2 = duplicate.copy()
			child2.placeTile(empty[0], empty[1], 2)
			statesList.append(child2)
			probsList.append(self.prob2 * 1. / numEmptyInd)

			child4 = duplicate.copy()
			child4.placeTile(empty[0], empty[1], 4)
			statesList.append(child4)
			probsList.append(self.prob4 * 1. / numEmptyInd)

		return (statesList, probsList)

	def manhattanDistance(self, pos1, pos2):
		x1, y1 = pos1
		x2, y2 = pos2
		return np.abs((x2 - x1)) + np.abs((y2 - y1))
