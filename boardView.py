import pygame

class BoardView():
	"""
	A pygame view for the board state.
	"""

	def __init__(self, width, height, size, fontFamily="freesansbold.ttf", fontSize=30,
				 backgroundColor=(155, 155, 155)):
		"""
		Initialize a BoardView instance.
		"""
		pygame.init()
		pygame.font.init()
		self.font = pygame.font.Font(fontFamily, fontSize)
		self.backgroundColor = backgroundColor
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode([self.width, self.height])
		pygame.display.set_caption('2048')

		self.size = size
		self.blockWidth = 1. * self.width / self.size
		self.blockHeight = .8 * self.height / self.size
		self.blockColors = {2: (125,125,0)}

	def render(self, board):

		# draw background
		self.screen.fill(self.backgroundColor)

		self.drawBoard(board)

		self.drawScore(board.score)


	def drawBoard(self, board):
		"""
		Draw the board.
		"""

		# draw each square
		for i in range(board.size):
			for j in range(board.size):
				self.drawSquare(i, j, board.grid[i][j], board)

	def drawScore(self, score):
		textSurf, textRect = self.textObjects("Score: " + str(score))
		textRect.center = (self.width / 2., self.height * .9)
		self.screen.blit(textSurf, textRect)

	def drawSquare(self, i, j, val, board):
		if val == 0:
			pygame.draw.rect(self.screen, (155,155,155), 
						((j + .1) * self.blockWidth, (i + .1) * self.blockHeight, 
						.8 * self.blockWidth, .8 * self.blockHeight))
			return 

		color = self.getColorVal(val)
		pygame.draw.rect(self.screen, color, 
						((j + .1) * self.blockWidth, (i + .1) * self.blockHeight, 
						.8 * self.blockWidth, .8 * self.blockHeight))

		textSurf, textRect = self.textObjects(str(val))
		textRect.center = ((j + .5) * self.blockWidth, (i + .5) * self.blockHeight)
		self.screen.blit(textSurf, textRect)

	def getColorVal(self, val):
		for i in range(14):
			if val == 2 ** i:
				return (255, 220 - 10 * i, 0)

	def textObjects(self, text):
	    textSurface = self.font.render(text, True, (0,0,0))
	    return textSurface, textSurface.get_rect()
