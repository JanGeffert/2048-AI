import numpy as np
import sys
from agents import *
from collections import Counter
from evaluators import Evaluator

class qLearningAgent(Agent):
	""" Abstract class for Q-Learning Agent """


	def __init__(self, startState, alpha=1.0, epsilon=0.05, 
				 gamma=0.8, iters=1000):
		""" 
		Initialize qLearningAgent 
		startState = to be used to train Q-learning agent
		alpha = learning rate
		epsilon = exploration probability
		gamma = discounting future reward
		iters = number of iterations to train q-learning agent
		"""

		self.alpha = alpha
		self.epsilon = epsilon
		self.gamma = gamma
		self.iters = iters
		self.startState = startState

		# (eval_function : weight)
		self.weights = Counter()
		super().__init__()

	def getQValue(self, state, move):
		"""
		Returns the q-Value for a given state-move pair by executing our
		approximating Q(s, a) function
		"""
		# COPY BOARD
		# EXECUTE ACTION, 
		# GET new_state

		# Takes into account current weights as well
		return Evaluator.evaluate(new_state)

		# return self.qValues[(state, move)]

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

		bestMove = None
		
		# Check if no valid moves
		if state.isGameOver():
			return bestMove

		# Store valid moves
		moves = state.validMoves()
		
		# Flip coin to determine if random move
		if np.random.random() < self.epsilon:
			bestMove = np.random.choice(moves)
		else:
			bestMove = self.findBestMove(state)

		return bestMove

	def getReward(self, state):
		"""
		Calculate the reward for being in a certain state.
		"""
		return state.score

	def update_weights(state):
		move = self.move(state)
		q = self.getQValue(state, move)
		# COPY BOARD TO EXECUTE move
		new_state = EXECUTE(state, move)

        # Get best move (findBestMove maximizes Q value)
        r = self.getReward(new_state)
        action_prime = self.findBestMove(state)

        difference = r + self.gamma * self.getQValue(new_state, action_prime) - q

        for eval_func in self.weights.keys():
        	self.weights[eval_func] = self.weights[eval_func] + self.alpha * difference * Evaluator().method(eval_func)(state, move)

