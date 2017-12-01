import numpy as np
import sys

class Evaluator():

	"""

	Sample Dict
	{
		"score": 42
		"maxTile": 1
		"numEmpty": 1
		"maxTileCorner": 2
		"tileDiff": 13
		"monotonicity": 25
		"snakeMonotonicity": 10
		"logScore": 0
		"fullMaxRow": 23
	}
	"""

	def uniformWeights():
		"""Return a weight dictionary with all features and weights 1,1,1.."""
		weights = {"score": 1, "maxTile": 1, "numEmpty": 1, "maxTileCorner": 1,
					"tileDiff": 13, "monotonicity": 25, "snakeMonotonicity": 10,
					"logScore": 0, "fullMaxRow": 23}
		return weights

	def evaluate(state, weights):
		value = 0
		for (feature, weight) in weights.items():
			if weight > 0:
				try:
					value += weight * getattr(Evaluator, feature)(state)
				except:
					pass
		return value

	def score(state):
		return state.score

	def maxTile(state):
		return state.maxTile()

	def numEmpty(state):
		return state.numberEmpty()

	def maxTileCorner(state):
		maxPos = state.maxTilePosition()
		cornerPos = (state.size-1, state.size-1)
		dist = state.manhattanDistance(cornerPos, maxPos)
		return -1. * dist

	def tileDiff(state):
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

	def monotonicity(state):
		"""Return the degree to which the board is monotonic"""

		def rowDiff(stateRow):
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

		# Optimal monotonicity for maximum in bottom-right corner
		totalDiff = 0

		for i in range(state.size):
			# Penalize rows closer to max tile more
			totalDiff += rowDiff(state.grid[i]) * (state.size - i)
			col = []
			for row in range(state.size):
				col.append(state.grid[row][i])
			totalDiff += rowDiff(col) * i

		return -1 * totalDiff

	def snakeMonotonicity(state):
		"""Return the degree to which the board is monotonic in an S shape,
		increasing from top left until bottom left in the following shape:
		1234
		8765
		9ABC
		GFED
		"""

		# Optimal monotonicity for maximum in bottom-right corner
		totalDiff = 0

		positions = []
		for row in range(4):
			if row%2 == 0:
				positions += [(row, i) for i in range(4)]
			else:
				positions += [(row, i) for i in reversed(range(4))]

		for i in range(1, len(positions)):
			currVal = np.log2(state.grid[positions[i][0]][positions[i][1]] + 1)
			prevVal = np.log2(state.grid[positions[i - 1][0]][positions[i - 1][1]] + 1)

			if currVal < prevVal:
				totalDiff += (prevVal - currVal) * prevVal

		return -1 * totalDiff

	def logScore(state):
		"""Returns the log base two of the current score."""
		if state.score == 0:
			return 0

		return np.log2(state.score)

	def fullMaxRow(state):
		""" Returns how full the row with the max tile is. """
		rowIndex, colIndex = state.maxTilePosition()
		empty = 0
		for col in range(state.size):
			if state.grid[rowIndex][col] == 0:
				empty += 1
		return -1 * empty
