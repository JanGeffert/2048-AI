import numpy as np
import sys

class Agent():
	"""
	A general agent that plays a 2048 game.
	Note that this agent is supposed to be to be subclassed.
	"""

	def __init__(self):
		"""Initialize an agent"""
		self.scores = []
		self.maxTiles = []

	def move(self, board):
		"""
		Return the agents move (LEFT, RIGHT, UP, DOWN)
		given a certain board state.
		"""
		pass

	def addScore(self, score):
		"""
		Add the current score of the game to an internal representation.
		"""
		self.scores.append(score)

	def addMaxTile(self, tile):
		"""
		Add the value of the current maxTile of the game to an internal
		representation.
		"""
		self.maxTiles.append(tile)


class RandomAgent(Agent):
	"""
	A random agent which chooses any of the valid moves with equal probability.
	"""

	def move(self, board):
		"""Return a any of the valid moves with equal probability"""
		return np.random.choice(board.validMoves())


class HeuristicAgent(Agent):
	"""
	A greedy agent which chooses a moved based on maximizing a specified
	heuristic function.
	"""

	def __init__(self, fn="MaxTile"):
		"""
		Initialize a heuristic agent with one of the following heuristics:
			* fn="MaxTile" the value of the maximum tile (default)
			* fn="NumEmpty" the number of empty squares
		"""
		self.fn = fn
		super().__init__()

	def findChild(self, move, state):
		child = state.copy()
		child.updateBoard(move, printOpts=False)
		return child

	def findValue(self, state, ply=0):
		if ply == 0:
			if self.fn == "MaxTile":
				return state.maxTile()
			elif self.fn == "NumEmpty":
				return state.numberEmpty() * state.maxTile()
			else:
				return 0
		else:
			actions = state.validMoves()
			children = [self.findChild(action, state) for action in actions]
			return max([self.findValue(child, ply=ply - 1) for child in children], 0)

	def move(self, state):
		bestVal = -sys.maxsize
		bestAction = None
		for action in state.validMoves():
			val = self.findValue(self.findChild(action, state))
			if val > bestVal:
				bestVal = val
				bestAction = action
		return action


class ExpectimaxAgent(Agent):

	def __init__(self, depth=1, fn="MaxTile"):
		self.fn = fn
		self.depth = depth
		super().__init__()

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
		bestVal = -sys.maxsize
		bestAction = None
		for action in state.validMoves():
			val = self.findValue(self.findChild(action, state), self.depth)
			if val > bestVal:
				bestVal = val
				bestAction = action
		return action
