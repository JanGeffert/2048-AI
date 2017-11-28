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

class MonteCarloAgent(Agent):
	"""
	An agent which chooses a move, based on which move would be best according to
	200 random rollouts.
	"""

	def __init__(self, rollouts=10):
		self.rollouts = rollouts
		super().__init__()

	def move(self, board):
		"""Return a any of the valid moves with equal probability"""

		bestScore = board.score
		bestMove = None
		for move in board.validMoves():
			# print("Trying out {}".format(move))
			score = self.rollout(move, board)
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

""" ------------------------------------ """
""" Linear Combination Expectimax Agents """
""" ------------------------------------ """

class ComboExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent that uses a linear combination
	of heuristic functions.
	"""

	def __init__(self, maxScore=0, maxTile=0, numEmpty=10,
				 corner=0, tileDiff=0, logScore=0,
				 monotonicWeight=1):

		# Store weights for functions
		self.maxScore = maxScore
		self.maxTile = maxTile
		self.numEmpty = numEmpty
		self.corner = corner
		self.tileDiffWeight = tileDiff
		self.logScoreWeight = logScore
		self.monotonicWeight = monotonicWeight

		super().__init__()

	def cornerVal(self, state):
		maxPos = state.maxTilePosition()
		cornerPos = (0,0)
		dist = state.manhattanDistance(cornerPos, maxPos)
		return -1. * dist

	def tileDiff(self, state):
		"""
		Returns the total difference between the values of
		neighboring tiles.
		"""
		diff = 0
		for i in range(state.size):
			for j in range(state.size):
				neighbors = state.getNeighbors((i,j))
				for x, y in neighbors:
					val1 = state.grid[x][y]
					val2 = state.grid[i][j]
					if val1 != 0:
						val1 = int(np.log2(val1))
					if val2 != 0:
						val2 = int(np.log2(val2))

					diff += np.abs(val1 - val2)
		return diff

	def rowDiff(self, stateRow):
		""" Returns the severity of the differences breaking
		monotonicity within a row. """

		diff = 0

		logVals = [np.log2(i + 1) for i in stateRow]
		prevVal = 0
		val = 0
		for i in range(len(logVals)):
			val = logVals[i]
            # if monotonicity is broken, penalize
			if val < prevVal:
				diff += (prevVal - val) * prevVal
			prevVal = val
		return diff

	def monotonicScore(self, state):
		"""Return the degree to which the board is monotonic"""

        # Optimal monotonicity for maximum in top-right corner

		# 1243
		# 0023
		# 0002
		# 0000

        # penalties should be higher for violations close to maximum
		totalDiff = 0

		for i in range(state.size):
			# Penalize rows closer to max tile more
			totalDiff += self.rowDiff(state.grid[i]) * (state.size - i)
			col = []
			for row in range(state.size):
				col.append(state.grid[row][i])
			totalDiff += self.rowDiff(col) * i

		return -1 * totalDiff


	def logScore(self, state):
		"""Returns the log base two of the current score."""
		if state.score == 0:
			return 0

		return np.log2(state.score)

	def valueFunction(self, state):
		value = 0
		value += self.maxScore * state.score
		value += self.logScoreWeight * self.logScore(state)
		value += self.maxTile * state.maxTile()
		value += self.numEmpty * state.numberEmpty()
		value += self.corner * self.cornerVal(state)
		value += self.tileDiffWeight * -1 * self.tileDiff(state)
		value += self.monotonicWeight * self.monotonicScore(state)
		return value

class TileDiffExpectimaxAgent(ComboExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the TODO.
	"""
	def __init__(self):
		super.__init__(maxScore=0, maxTile=0, numEmpty=1, corner=0, tileDiff=-1)
