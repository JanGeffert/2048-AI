import numpy as np
import sys
from agents import *
from collections import Counter
from evaluators import Evaluator

class QLearningAgent(Agent):
	""" Abstract class for Q-Learning Agent """


	def __init__(self, alpha=1.0, epsilon=0.05, 
				 gamma=0.8):
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
		self.weights = Evaluator.uniformWeights()
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
		bestQValue = - float("inf")

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

		# Store valid moves
		moves = state.validMoves()
		
		# Flip coin to determine if random move
		if np.random.random() < self.epsilon:
			bestMove = np.random.choice(moves)
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
		q = self.getQValue(state, self.prevMove)
		
		# newState = state.getSuccessor(self.prevMove, printOpts=False)

		# Get best move (findBestMove maximizes Q value)
		r = self.getReward(self.prevState, self.prevMove, state)
		actionPrime = self.findBestMove(state)
		maxQ = self.getQValue(state, actionPrime)

		difference = r + self.gamma * self.getQValue(state, actionPrime) - q

		for feature in self.weights.keys():
			self.weights[feature] = self.weights[feature] + self.alpha * difference * getattr(Evaluator, feature)(state)

		print(self.weights)
