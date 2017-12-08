import numpy as np
import sys
from multiprocessing import Pool
from evaluators import Evaluator

class Agent():
	"""
	A general agent that plays a 2048 game.
	Note that this agent is supposed to be to be subclassed.
	"""

	def __init__(self, depth=2):
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

class MonteCarloAgent(Agent):
	"""
	An agent which chooses a move, based on which move would be best according to
	200 random rollouts.
	"""

	def __init__(self, rollouts=200):
		self.rollouts = rollouts
		super().__init__()

	def move(self, board):
		"""Return a any of the valid moves with equal probability"""

		bestScore = board.score
		bestMove = None
		for move in board.validMoves():
			# print("Trying out {}".format(move))
			score = self.multiProcessingRollout(move, board)
			if score > bestScore:
				bestScore = score
				bestMove = move

		return bestMove

	def rollout(self, move, board):
		"""Return the average score of a randomly played game after making one specific move
		(self.rollouts)."""
		scores = []
		for _ in range(self.rollouts):
			postMoveBoard = board.getSuccessor(move, printOpts=False)
			while len(postMoveBoard.validMoves()) > 0:
				postMoveBoard = postMoveBoard.getSuccessor(np.random.choice(postMoveBoard.validMoves()), printOpts=False)
			scores.append(postMoveBoard.score)

		return np.mean(scores)

	def multiProcessingRollout(self, move, board):
		"""Return the average score of a randomly played game after making one specific move
		(self.rollouts). Note: this function distributes rollouts onto different cores."""

		scores = []
		pool = Pool(processes=4)
		scores = pool.map(simulateMC, [(board, move) for _ in range(self.rollouts)])
		pool.close()
		return np.mean(scores)

def simulateMC(args):
	b, move = args
	postMoveBoard = b.getSuccessor(move, printOpts=False)
	while len(postMoveBoard.validMoves()) > 0:
		postMoveBoard = postMoveBoard.getSuccessor(np.random.choice(postMoveBoard.validMoves()), printOpts=False)
	return postMoveBoard.score


class ExpectimaxAgent(Agent):
	"""
	A greedy agent which chooses a moved based on maximizing a specified
	heuristic function.
	"""

	def __init__(self, weights, depth):
		"""
		Initialize an expectimax agent.
		"""
		self.weights = weights
		self.maxDepth = depth
		super().__init__()

	def valueFunction(self, state):
		return Evaluator.evaluate(state, self.weights)

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
	def __init__(self, depth):
		super().__init__({"score": 1}, depth)

class MaxTileExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the maximum tile.
	"""
	def __init__(self, depth):
		super().__init__({"maxTile": 1}, depth)


class NumEmptyExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the number
	of empty squares.
	"""
	def __init__(self, depth):
		super().__init__({"numEmpty": 1}, depth)


class MaxTileCornerExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to place the maximum valued
	tile in a corner of the board.
	"""
	def __init__(self, depth):
		super().__init__({"maxTileCorner": 1}, depth)

class MonotonicSnakeExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent that prefers full bottom row.
	"""
	def __init__(self, depth):
		super().__init__({"snakeMonotonicity": 1}, depth)

class FullMaxRowExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent that prefers full bottom row.
	"""
	def __init__(self, depth):
		super().__init__({"fullMaxRow": 1}, depth)

class TileDiffExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent trying to minimize adjacent tile differences
	throughout the board.
	"""
	def __init__(self, depth):
		super().__init__({"tileDiff": 1}, depth)

class AscendingRowsExpectimaxAgent(ExpectimaxAgent):
	"""
	Expectimax agent that orders values s.t. they are
	monotonically increasing across rows and columns
	"""
	def __init__(self, depth):
		super().__init__({"monotonicity": 1}, depth)

class WeightedExpectimaxAgent(ExpectimaxAgent):
	"""
	Expectimax agent that uses a linear combination of
	evaluation functions.
	"""
	def __init__(self, depth):
		super().__init__({"score": 7, "maxTile": 7, "numEmpty": 7, "corner": 5,
						  "tileDiff": 5, "logScore": 18, "monotonicity": 4}, depth)
