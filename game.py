# Import game objects
from gameObjects import *
# Import expectimax and random agents
from agents import *
# Import Q-Learning agents
from qLearningAgents import *

from logger import *
from boardView import *
from pygame import *

import time
import sys
import os
from graphUtils import *
import tqdm

class Game():
	"""A 2048 game."""

	def __init__(self, agent, depth=None, graphics=False, trials=1, dim=4, delayLength=0.1, webview=False):
		"""Initialize a new game."""

		self.graphics = graphics
		self.trials = trials
		self.dim = dim

		# Instantiate agent
		if depth is None or agent == "MonteCarloAgent" or "QLearningAgent":
			self.agent = eval(agent)()
		else:
			self.agent = eval(agent)(depth=depth)
		# Instantiate board
		self.board = Board(size=dim)
		# Create Log File for agent
		self.logName = beginLog(self.board)
		if self.graphics:
			# Create a board view instance
			self.view = BoardView(size=dim)
			self.delay = delayLength
		else:
			self.view = None
			self.delay = 0

		if webview:
			os.system("python replay.py {}".format(self.logName))


	def run(self):
		"""Plays the specified number of games with the agent."""

		# Play certain number of trials
		for trial in tqdm.trange(self.trials):
			while True:
				if self.graphics:
					# Create grid of squares
					self.view.render(self.board)
					pygame.display.update()

				if self.board.isGameOver():
					if type(self.agent).__name__ == "QLearningAgent":
						self.agent.prevMove, self.agent.prevState = None, None
						print(self.agent.weights)
					# print("You lose! Your score was {}".format(self.board.score))
					# print("Your highest tile was: {}".format(self.board.maxTile()))

					# Keep track of agent's performance
					self.agent.addScore(self.board.score)
					self.agent.addMaxTile(self.board.maxTile())
					log(self.logName, self.board, decisionTime, self.agent, "N/A", trial)
					break

				beginTime = time.time()
				move = self.agent.move(self.board)
				endTime = time.time()

				decisionTime = endTime - beginTime

				# Log state
				log(self.logName, self.board, decisionTime, self.agent, move, trial)

				self.board = self.board.getSuccessor(move, printOpts=False)
				time.sleep(self.delay)

				if self.graphics:
					events = pygame.event.get()
					for e in events:
						if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
							pygame.quit()
							sys.exit("Leaving because you requested it.")

			# Initialize new board
			self.board.initBoard()

		if self.graphics:
			pygame.quit()

		# Display results
		plotScoresMaxTiles(self.agent.scores, self.agent.maxTiles)
