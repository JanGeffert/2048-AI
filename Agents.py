from gameObjects import *
from agentPlayers import *
import time
import sys
from graphUtils import *
import tqdm

def AI2048(XDIM, YDIM, pprint=False, trials=1, player="random", fn="MaxTile"):

	pygame.init()
	pygame.font.init()

	font = pygame.font.Font('freesansbold.ttf', 30)

	if player == "random":
		agent = RandomAgent()
	elif player == "heuristic":
		agent = HeuristicAgent(fn=fn)
	elif player == "expectimax":
		agent = ExpectimaxAgent(depth=4, fn=fn)
	else:
		print("Player not implemented.  Type -h for help.")
		sys.exit()

	# Check if user wants graphics displayed
	if pprint:

		screen = pygame.display.set_mode([XDIM, YDIM])
		pygame.display.set_caption('2048')
		screen.fill((155,155,155))

		sleepTime = .1

		displayScreen = True

		board = Board(XDIM, int(YDIM * .8))

	else:

		board = Board(XDIM, YDIM)
		sleepTime = 0
		displayScreen = False

	# Play certain number of trials
	for _ in tqdm.trange(trials):
		while True:

			if displayScreen:
				# Create grid of squares
				screen.fill((155,155,155))

				drawBoard(board, screen)

				TextSurf, TextRect = text_objects("Score: " + str(board.score), font)
				TextRect.center = (XDIM / 2., YDIM * .9)
				screen.blit(TextSurf, TextRect)

				pygame.display.update()

			if board.isGameOver():
				# print("You lose! Your score was {}".format(board.score))
				# print("Your highest tile was: {}".format(board.maxTile()))

				# Keep track of agent's performance
				agent.addScore(board.score)
				agent.addMaxTile(board.maxTile())

				break

			move = agent.move(board)

			board.updateBoard(move, printOpts=False)

			time.sleep(sleepTime)

			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
					sys.exit("Leaving because you requested it.")

		# Initialize new board
		board.initBoard()

	# Display results
	plotScoresMaxTiles(agent.scores, agent.maxTiles)

	

