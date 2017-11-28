from gameObjects import *
from game import *
from pygame.locals import *
import sys
import argparse

availableAgents = [RandomAgent,
				   MaxScoreExpectimaxAgent,
				   MaxTileExpectimaxAgent,
				   NumEmptyExpectimaxAgent,
				   MaxTileCornerExpectimaxAgent,
				   TileDiffExpectimaxAgent,
				   ComboExpectimaxAgent,
				   MonteCarloAgent,
				   ComboMonteCarloAgent]

def main(agent, graphics=True, trials=1, dim=4, webview=False):
	game = Game(agent, graphics=graphics, trials=trials, dim=dim, webview=webview)
	game.run()

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Welcome to 2048, AI edition.')

	agentHelp = "Options: " + "\n".join(["{} ({}), ".format(agent.__name__, agent.__doc__.strip()) for agent in availableAgents])
	agentNames = [agent.__name__ for agent in availableAgents]

	parser.add_argument("agent", metavar="AGENT",
                    	help=agentHelp, choices=agentNames)
	parser.add_argument("-g", "--graphics", help="display graphics", action="store_true")
	parser.add_argument("-t", "--trials", default=1, type=int, help="number of times to play")
	parser.add_argument("-d", "--dimension", default=4, type=int, help="dimension of the board")
	parser.add_argument("-w", "--webview", help="display webview of replay", action="store_true")

	args = parser.parse_args()

	main(args.agent, graphics=args.graphics, trials=args.trials, dim=args.dimension, webview=args.webview)
