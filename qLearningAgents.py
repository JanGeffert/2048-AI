import numpy as np
import sys
from agents import *
from collections import Counter

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

		self.qValues = Counter()
		super().__init__()

		# OFFLINE LEARNING
		state = self.startState
		for i in self.iters:
			# Get move and nextState
			move = self.findBestMove(state)
			nextState = state.getSuccessor(move)

			# Check if game is over
			if state.isGameOver():
				reward = 0
				self.update(state, move, nextState, reward)
				break
			else:
				reward = self.getReward(state)
				self.update(state, move, nextState, reward)

				# Prepare for next iteration
				state = nextState
			
			# Rudimentary progress report
			if i == self.iters / 10:
				print("10% Complete Training")
			elif i == self.iters / 2:
				print("50% Complete Training")

	def update(self, state, move, nextState, reward):
		"""
		Here is where the q-value iteration takes place.
		"""
		# Store best next action
		bestNextAction = self.findBestMove(nextState)
		# Store best next q-Value
		bestQVal = self.qValues[(nextState, bestNextAction)]

		# Update current q-Value
		self.qValues[(state, move)] = \
			(1 - self.alpha) * self.qValues[(state, move)] + \
			self.alpha * (reward + self.gamma * bestQVal)

	def getReward(self, state):
		"""
		Calculate the reward for being in a certain state.
		"""
		pass

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

	def getQValue(self, state, move):
		"""
		Returns the q-Value for a given state-move pair.
		"""

		return self.qValues[(state, move)]

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

