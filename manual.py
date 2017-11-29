from gameObjects import *
from boardView import *
from pygame import *
import sys

def manual2048(XDIM, YDIM, pprint=False):

	# Create a board view instance
	view = BoardView(XDIM, YDIM, size=4)

	# Check if user wants graphics displayed
	if pprint:
		board = Board(size=4)
		displayScreen = True
	else:
		board = Board(size=4)
		print(board)
		displayScreen = False

	# Create Log File for agent
	logName = beginLog(board)

	while True:
		if displayScreen:
			view.render(board)
			pygame.display.update()

		if board.isGameOver():
			print("You lose! Your score was {}".format(board.score))
			print("Your highest tile was: {}".format(board.maxTile()))
			log(logName, board, "N/A", "N/A", "N/A", "N/A")
			break

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit("Leaving because you requested it.")
			if event.type == KEYUP:
				if event.key == K_UP:
					# Log state
					log(logName, board, "N/A", "N/A", "UP", "N/A")
					board = board.getSuccessor("UP", printOpts=(not pprint))
				elif event.key == K_DOWN:
					# Log state
					log(logName, board, "N/A", "N/A", "DOWN", "N/A")
					board = board.getSuccessor("DOWN", printOpts=(not pprint))
				elif event.key == K_LEFT:
					# Log state
					log(logName, board, "N/A", "N/A", "LEFT", "N/A")
					board = board.getSuccessor("LEFT", printOpts=(not pprint))
				elif event.key == K_RIGHT:
					# Log state
					log(logName, board, "N/A", "N/A", "RIGHT", "N/A")
					board = board.getSuccessor("RIGHT", printOpts=(not pprint))
				else:
					continue
