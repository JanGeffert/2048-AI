import numpy as np
import sys
from agents import *
from collections import Counter
from evaluators import Evaluator

class QLearningAgent(Agent):
	""" Abstract class for Q-Learning Agent """


	def __init__(self, alpha=0.01, epsilon=0.05,
				 gamma=0.95):
		"""
		Initialize qLearningAgent
		alpha = learning rate
		epsilon = exploration probability
		gamma = discounting future reward
		iters = number of iterations to train q-learning agent
		"""

		self.alpha = alpha
		self.epsilon = epsilon
		self.gamma = gamma
		self.prevState = None
		self.prevMove = None

		# (eval_function : weight)
		# self.weights = Evaluator.uniformWeights()
		# self.weights = {"numEmpty": 1, "monotonicity": 1, "logScore": 1}
		self.weights = {"score": 1}
		super().__init__()


	def getQValue(self, state, move):
		"""
		Returns the q-Value for a given state-move pair by executing our
		approximating Q(s, a) function
		"""
		nextState = state.getSuccessor(move, printOpts=False)

		# Takes into account current weights as well
		return Evaluator.evaluate(nextState, self.weights)

	def findBestMove(self, state):
		"""
		Returns the best move given a state.
		"""

		# Check if no valid moves
		if state.isGameOver():
			return None

		# Store valid moves
		moves = state.validMoves()

		# Placeholder values
		bestMove = None
		bestQValue = -float("inf")

		# Find best move
		for move in moves:
			tempQVal = self.getQValue(state, move)
			if tempQVal > bestQValue:
				bestQValue = tempQVal
				bestMove = move

		return bestMove

	def move(self, state):
		"""
		Return the agents move (LEFT, RIGHT, UP, DOWN)
		given a certain board state.
		"""

		if self.prevMove:
			self.updateWeights(state)

		# Flip coin to determine if random move
		if np.random.random() < self.epsilon:
			bestMove = np.random.choice(state.validMoves())
		else:
			bestMove = self.findBestMove(state)

		self.prevState = state
		self.prevMove = bestMove
		return bestMove

	def getReward(self, prevState, action, currState):
		"""
		Calculate the reward for being in a certain state.
		"""
		return currState.score - prevState.score


	def updateWeights(self, state):
        # Q(s,a)
		q = self.getQValue(self.prevState, self.prevMove)

		# Get best move (findBestMove maximizes Q value)
        # R(s,a,s')
		r = self.getReward(self.prevState, self.prevMove, state)
        # a' that maximizes Q(s',a')
		actionPrime = self.findBestMove(state)
        # Q(s', a')
		maxQ = self.getQValue(state, actionPrime)

		difference = r + self.gamma * maxQ - q

		for feature in self.weights.keys():
			self.weights[feature] = self.weights[feature] + self.alpha * difference * getattr(Evaluator, feature)(state)
