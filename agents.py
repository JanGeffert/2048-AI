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

class WeightedExpectimaxAgent(ExpectimaxAgent):
	"""
	An expectimax agent that uses a linear combination
	of heuristic functions.
	"""

	def __init__(self, depth=2, maxScore=7, maxTile=7, numEmpty=7,
				 corner=5, tileDiff=5, logScore=18,
				 monotonicWeight=4, maxRowWeight=0):

		# Store weights for functions
		self.maxScore = maxScore
		self.maxTile = maxTile
		self.numEmpty = numEmpty
		self.corner = corner
		self.tileDiffWeight = tileDiff
		self.logScoreWeight = logScore
		self.monotonicWeight = monotonicWeight
		self.fullMaxRowWeight = maxRowWeight

		super().__init__(depth=depth)

	def cornerVal(self, state):
		maxPos = state.maxTilePosition()
		cornerPos = (state.size-1, state.size-1)
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

        # Optimal monotonicity for maximum in bottom-right corner
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

	def fullMaxRow(self, state):
		""" Returns how full the row with the max tile is. """
		rowIndex, colIndex = state.maxTilePosition()
		empty = 0
		for col in range(state.size):
			if state.grid[rowIndex][col] == 0:
				empty += 1
		return -1 * empty

	def valueFunction(self, state):
		value = 0
		if self.maxScore > 0:
			value += self.maxScore * state.score
		if self.logScoreWeight > 0:
			value += self.logScoreWeight * self.logScore(state)
		if self.maxTile > 0:
			value += self.maxTile * state.maxTile()
		if self.numEmpty > 0:
			value += self.numEmpty * state.numberEmpty()
		if self.corner > 0:
			value += self.corner * self.cornerVal(state)
		if self.tileDiffWeight > 0:
			value += self.tileDiffWeight * -1 * self.tileDiff(state)
		if self.monotonicWeight > 0:
			value += self.monotonicWeight * self.monotonicScore(state)
		return value

class FullMaxRowAgent(WeightedExpectimaxAgent):
	"""
	An expectimax agent that prefers full bottom row.
	"""

	def __init__(self, depth=2):
		super().__init__(depth=depth, maxScore=0, maxTile=0, numEmpty=0,
						 corner=0, tileDiff=0, maxRowWeight=0)

class TileDiffExpectimaxAgent(WeightedExpectimaxAgent):
	"""
	An expectimax agent trying to maximize the TODO.
	"""
	def __init__(self, depth=2):
		super().__init__(depth=depth, maxScore=0, maxTile=0, numEmpty=1,
						 corner=10, tileDiff=1, maxRowWeight=10)

class AscendingRowsExpectimaxAgent(WeightedExpectimaxAgent):
    """
	Expectimax agent that orders values s.t. they are
	monotonically increasing across rows and columns
	"""
    def __init__(self, depth=2):
        super().__init__(
			depth=depth,
            maxScore=0, maxTile=0, numEmpty=0,
            corner=0, tileDiff=0, logScore=0,
            monotonicWeight=1
        )


class WeightedMonteCarloAgent(WeightedExpectimaxAgent):
	"""
	Combine Monte Carlo Rollouts with Heuristic Combinations
	"""

	def __init__(self, rollouts=10, maxDepth=2):
		self.rollouts = rollouts
		self.maxDepth = maxDepth
		super().__init__(maxScore=0, maxTile=0, numEmpty=10,
						 corner=10, tileDiff=10, maxRowWeight=100)

	def move(self, board):
		"""Return a any of the valid moves"""

		# If there are many empty squares
		self.numEmpty=1
		if board.numberEmpty() > board.size:
			return self.findBestMove(board, self.maxDepth)[0]

		# When few empty squares, use rollout method with heuristic
		else:
			self.numEmpty=1000
			return self.findBestMove(board, self.maxDepth + 2)[0]
			# self.numEmpty=1000
			# bestScore = -100000000
			# bestMove = None
			# for move in board.validMoves():
			# 	score = self.rollout(move, board)
			# 	if score > bestScore:
			# 		bestScore = score
			# 		bestMove = move
            #
			# return bestMove

	def rollout(self, move, board):
		"""Return the score of a heuristically played game after making
		one specific move (self.rollouts)."""
		score = -1000000
		postMoveBoard = board.getSuccessor(move, printOpts=False)
		for _ in range(self.rollouts):
			if len(postMoveBoard.validMoves()) > 0:
				postMoveBoard = postMoveBoard.getSuccessor(self.findBestMove(postMoveBoard, 2)[0], printOpts=False)
			else:
				return score
		return self.valueFunction(postMoveBoard)
