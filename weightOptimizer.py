# Import game objects
from gameObjects import *
# Import expectimax and random agents
from agents import *
# Import Q-Learning agents
from qLearningAgents import *

from logger import *
from boardView import *

import time
import sys
import os
from graphUtils import *
import tqdm
import random
import numpy as np

class WeightOptimizer():

	def __init__(self, trials=5, dim=4, iterations=100):
		self.trials = trials
		self.iterations = iterations
		self.board = Board(size=dim)

	def getNeighborConfigs(self, config, n=10):
		neighbors = []
		for _ in range(n):
			neighborConfig = config.copy()

			weight = random.choice(list(neighborConfig.keys()))

			neighborConfig[weight] += random.choice(list(range(-5, 5)))
			if neighborConfig[weight] < 0:
				neighborConfig[weight] = 0

			neighbors.append(neighborConfig)
		return neighbors

	def run(self, p=0.05):
		currentConfig = {
				  "maxScore": 0,
				  "maxTile": 0,
				  "numEmpty": 0,
				  "corner": 0,
				  "logScore": 0,
				  "monotonicWeight": 0,
				 }
		currentScore = 0

		for _ in range(self.iterations):
			scores = []
			neighbors = self.getNeighborConfigs(currentConfig) + [currentConfig]
			for i in tqdm.trange(len(neighbors)):
				scores.append(self.configScore(neighbors[i]))
			if currentScore < max(scores):
				currentConfig = neighbors[np.argmax(scores)]
				currentScore = max(scores)
			print(currentConfig, currentScore)

		return currentConfig

	def configScore(self, config):
		scores = []
		maxTiles = []
		# Instantiate agent
		self.agent = ComboExpectimaxAgent(maxScore = config["maxScore"],
										  maxTile = config["maxTile"],
										  numEmpty = config["numEmpty"],
										  corner = config["corner"],
										  tileDiff = 0,
										  logScore = config["logScore"],
										  monotonicWeight = config["monotonicWeight"])

		# Play certain number of trials
		for trial in range(self.trials):
			while True:
				if self.board.isGameOver():
					# Keep track of agent's performance
					scores.append(self.board.score)
					maxTiles.append(self.board.maxTile())
					break

				move = self.agent.move(self.board)
				self.board = self.board.getSuccessor(move, printOpts=False)
			# Initialize new board
			self.board.initBoard()

		return np.mean(maxTiles)

optimizer = WeightOptimizer()
print(optimizer.run())
