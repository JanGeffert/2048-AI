from gameObjects import *
from agentPlayers import *
from logger import *
from boardView import *
from pygame import *

import time
import sys
from graphUtils import *
import tqdm

def AI2048(XDIM, YDIM, pprint=False, trials=1, agent="random", fn="MaxTile"):

	# Create a board view instance
	view = BoardView(XDIM, YDIM, size=4)

	# determine which agent is to be used
	if agent == "random":
		agent = RandomAgent()
	elif agent == "heuristic":
		agent = HeuristicAgent(fn=fn)
	elif agent == "expectimax":
		agent = ExpectimaxAgent(depth=4, fn=fn)
	else:
		print("Agent not implemented. Type -h for help.")
		sys.exit()

	# Check if user wants graphics displayed
	if pprint:
		sleepTime = .01
		displayScreen = True
		board = Board(size=4)
	else:
		board = Board(size=4)
		sleepTime = 0
		displayScreen = False

	# Create Log File for agent
	logName = beginLog(board)

	# Play certain number of trials
	for trial in tqdm.trange(trials):
		while True:

			if displayScreen:
				# Create grid of squares
				view.render(board)
				pygame.display.update()

			if board.isGameOver():
				# print("You lose! Your score was {}".format(board.score))
				# print("Your highest tile was: {}".format(board.maxTile()))

				# Keep track of agent's performance
				agent.addScore(board.score)
				agent.addMaxTile(board.maxTile())
				break

			move = agent.move(board)

			# Log state
			log(logName, board, agent, move, trial)
			board.updateBoard(move, printOpts=False)
			time.sleep(sleepTime)
			events = pygame.event.get()
			for e in events:
				if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
					pygame.quit()
					sys.exit("Leaving because you requested it.")

		# Initialize new board
		board.initBoard()

	pygame.quit()
	# Display results
	plotScoresMaxTiles(agent.scores, agent.maxTiles)




