import copy
import pygame
import numpy as np
from pygame.locals import *
from sets import Set

class Board():

	def __init__(self, XDIM, YDIM, size=4):

		self.XDIM = XDIM
		self.YDIM = YDIM

		self.size = size
		self.prob2 = .9
		self.prob4 = 1 - self.prob2

		self.blockWidth = 1. * XDIM / size
		self.blockHeight = 1. * YDIM / size
		self.blockColors = {2: (125,125,0)}

		self.LEFT = "LEFT"
		self.RIGHT = "RIGHT"
		self.UP = "UP"
		self.DOWN = "DOWN"

		self.grid = [[0] * x for x in [size] * size ]
		self.score = 0

		# Initialize random grid with either 2 or 3 blocks
		numberStart = np.random.randint(1, 4)
		self.genNewBlocks(numberStart)

	def __str__(self):
		totString = ""
		for i in xrange(self.size):
			rowString = "|"
			for j in xrange(self.size):
				rowString += str(self.grid[i][j]) + "|"
			totString += rowString + "\n"
		return totString

	def copy(self):
		return copy.deepcopy(self)

	def initBoard(self):
		self.grid = [[0] * x for x in [self.size] * self.size ]
		self.score = 0

		numberStart = np.random.randint(1, 4)
		self.genNewBlocks(numberStart)

	def findFree(self):
		freeSquares = []
		for i in xrange(self.size):
			for j in xrange(self.size):
				if self.grid[i][j] == 0:
					freeSquares.append(i * self.size + j)
		return freeSquares

	def findValidMoves(self):
		moves = Set([])
		
		for i in xrange(self.size):
			for j in xrange(self.size):
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
		return moves

	def updateBoard(self, move, printOpts=True):
		if move in self.findValidMoves():
			if move == self.LEFT:
				# Shift all rows left
				for i in xrange(self.size):
					self.grid[i], newVal = self.moveLeft(self.grid[i])
					self.score += newVal
			if move == self.RIGHT:
				for i in xrange(self.size):
					self.grid[i], newVal = self.moveRight(self.grid[i])
					self.score += newVal
			if move == self.DOWN:
				for j in xrange(self.size):
					col, newVal = self.moveDown([row[j] for row in self.grid])
					self.score += newVal
					for i, row in enumerate(self.grid):
						row[j] = col[i]
			if move == self.UP:
				for j in xrange(self.size):
					col, newVal = self.moveUp([row[j] for row in self.grid])
					self.score += newVal
					for i, row in enumerate(self.grid):
						row[j] = col[i]
			self.genNewBlocks(1)
		if printOpts:
			print self, "Score: {}".format(self.score)

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

	def genNewBlocks(self, num):
		freeSquares = self.findFree()
		locations = np.random.choice(freeSquares, size=num, replace=False)
		for loc in locations:
			j = loc % self.size
			i = (loc - j) / self.size
			choice = np.random.random()
			if choice > 1 - self.prob2:
				self.grid[i][j] = 2
			else:
				self.grid[i][j] = 4

	def isGameOver(self):
		moves = self.findValidMoves()
		if len(moves) == 0:
			return True
		else:
			return False

	def maxTile(self):
		maxT = 0
		for i in xrange(self.size):
			for j in xrange(self.size):
				val = self.grid[i][j]
				if val > maxT:
					maxT = val
		return maxT

	def secondHighestTile(self):

		flat = sorted(np.array(self.grid).flatten())
		return flat[1] + flat[0] + flat[2]


	def numberEmpty(self):
		tot = 0
		for i in xrange(self.size):
			for j in xrange(self.size):
				if self.grid[i][j] == 0:
					tot += 1
		return tot

	def placeBlock(self, i, j, val):
		self.grid[i][j] = val

	def allPossibleNextStates(self):
		futureBoards = []
		numEmpty = self.numberEmpty()
		for i in xrange(self.size):
			for j in xrange(self.size):
				if self.grid[i][j] == 0:
					board2 = self.copy()
					board4 = self.copy()

					board2.placeBlock(i, j, 2)
					b2prob = 1 / numEmpty * self.prob2

					board4.placeBlock(i, j, 4)
					b4prob = 1 / numEmpty * self.prob4

					futureBoards.append((board2, b2prob))
					futureBoards.append((board4, b4prob))
		return futureBoards


""" ************************************ """

# Drawing the object
pygame.init()
pygame.font.init()

font = pygame.font.Font('freesansbold.ttf', 30)

def drawBoard(board, screen):
	for i in xrange(board.size):
		for j in xrange(board.size):
			drawSquare(i, j, board.grid[i][j], screen, board)

def drawSquare(i, j, val, screen, board):
	if val == 0:
		pygame.draw.rect(screen, (155,155,155), 
					((j + .1) * board.blockWidth, (i + .1) * board.blockHeight, 
					.8 * board.blockWidth, .8 * board.blockHeight))
		return 

	color = getColorVal(val)
	pygame.draw.rect(screen, color, 
					((j + .1) * board.blockWidth, (i + .1) * board.blockHeight, 
					.8 * board.blockWidth, .8 * board.blockHeight))

	TextSurf, TextRect = text_objects(str(val), font)
	TextRect.center = ((j + .5) * board.blockWidth, (i + .5) * board.blockHeight)
	screen.blit(TextSurf, TextRect)

def getColorVal(val):
	for i in xrange(14):
		if val == 2 ** i:
			return (255, 220 - 10 * i, 0)


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

