import numpy as np

MININT = -100000000

class Agent():

	def __init__(self):
		self.scores = []
		self.maxTiles = []

	def move(self, board):
		pass

	def addScore(self, score):
		self.scores.append(score)

	def addMaxTile(self, tile):
		self.maxTiles.append(tile)


class RandomAgent(Agent):

	def __init__(self):
		self.scores = []
		self.maxTiles = []

	def move(self, board):
		move = np.random.choice(list(board.findValidMoves()))
		return move

class HeuristicAgent(Agent):

	def __init__(self, fn="MaxTile"):
		self.scores = []
		self.maxTiles = []
		self.fn = fn

	def findChild(self, move, state):
		child = state.copy()
		child.updateBoard(move, printOpts=False)
		return child

	def findValue(self, state, ply=0):
		if ply == 0:
			if self.fn == "MaxTile":
				return state.secondHighestTile()
			elif self.fn == "NumEmpty":
				return state.numberEmpty() * state.maxTile()
			else:
				return 0
		else:
			actions = state.findValidMoves()
			children = [self.findChild(action, state) for action in actions]
			return max([self.findValue(child, ply=ply - 1) for child in children], 0)

	def move(self, state):
		bestVal = MININT
		bestAction = None
		for action in list(state.findValidMoves()):
			val = self.findValue(self.findChild(action, state))
			if val > bestVal:
				bestVal = val
				bestAction = action
		return action


class ExpectimaxAgent(Agent):

	def __init__(self, depth=1, fn="MaxTile"):
		self.scores = []
		self.maxTiles = []

		self.fn = fn

		self.depth = depth

	def findChild(self, move, state):
		child = state.copy()
		child.updateBoard(move, printOpts=False)
		return child

	def findValue(self, state, depth):
		if depth == 0:
			if self.fn == "MaxTile":
				return state.maxTile()
			elif self.fn == "NumEmpty":
				return state.numberEmpty()
			else:
				return 0

		val = 0
		childrenProbs = state.allPossibleNextStates()
		for child, prob in childrenProbs:
			val += prob * self.findValue(child, depth - 1)
		return val

	def move(self, state):
		bestVal = MININT
		bestAction = None
		for action in list(state.findValidMoves()):
			val = self.findValue(self.findChild(action, state), self.depth)
			if val > bestVal:
				bestVal = val
				bestAction = action
		return action
