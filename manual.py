from gameObjects import *
import sys

def manual2048(XDIM, YDIM, pprint=False):

	pygame.init()
	pygame.font.init()

	font = pygame.font.Font('freesansbold.ttf', 30)

	# Check if user wants graphics displayed
	if pprint:
		screen = pygame.display.set_mode([XDIM, YDIM])
		pygame.display.set_caption('2048')
		screen.fill((155,155,155))

		board = Board(XDIM, int(YDIM * .8))

		displayScreen = True

	else:

		board = Board(XDIM, YDIM)
		print board
		displayScreen = False

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
			print "You lose! Your score was {}".format(board.score)
			print "Your highest tile was: {}".format(board.maxTile())
			break

		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
				sys.exit("Leaving because you requested it.")
			if (e.type == KEYUP and e.key == K_UP):
				board.updateBoard("UP", printOpts=(not pprint))
			if (e.type == KEYUP and e.key == K_DOWN):
				board.updateBoard("DOWN", printOpts=(not pprint))
			if (e.type == KEYUP and e.key == K_LEFT):
				board.updateBoard("LEFT", printOpts=(not pprint))
			if (e.type == KEYUP and e.key == K_RIGHT):
				board.updateBoard("RIGHT", printOpts=(not pprint))


