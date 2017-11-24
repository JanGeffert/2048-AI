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


class ExpectimaxAgent(Agent):
	"""
	A greedy agent which chooses a moved based on maximizing a specified
	heuristic function.
	"""

	def __init__(self, depth=2):
		"""
		Initialize an expectimax agent.
		"""
		self.maxDepth = depth
		super().__init__()

	def valueFunction(self, state):
		pass

	def findBestMove(self, state, depth):
		if depth == 0 or state.isGameOver():
			return None, self.valueFunction(state)

		moves = state.validMoves()
		successorProbs = [state.getAllSuccessors(move) for move in moves]

		bestMove = None
		bestVal = -sys.maxsize

		for i, (successors, probs) in enumerate(successorProbs):

			values = [self.findBestMove(successor, depth - 1)[1] * prob for 
						(successor, prob) in zip(successors, probs)]
			expectedValue = np.sum(values)
			if expectedValue > bestVal:
				bestVal = expectedValue
				bestMove = moves[i]
		return bestMove, bestVal

	def move(self, state):
		"""
		Greedily choose the action that maximizes the heuristic.
		"""
		return self.findBestMove(state, self.maxDepth)[0]


class MaxScoreExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the score.
	"""
	def valueFunction(self, state):
		return state.score


class MaxTileExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the maximum tile.
	"""
	def valueFunction(self, state):
		return state.maxTile()


class NumEmptyExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the number
	of empty squares.
	"""
	def valueFunction(self, state):
		return state.numberEmpty()


class MaxTileCornerExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the TODO.
	"""

	def valueFunction(self, state):
		maxPos = state.maxTilePosition()
		cornerPos = (0,0)
		dist = state.manhattanDistance(cornerPos, maxPos)
		return -1. * dist


class TileDiffExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the TODO.
	"""
	def valueFunction(self, state):
		return -1 * state.tileDiff()

