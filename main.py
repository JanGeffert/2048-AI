from gameObjects import *
from manual import *
from Agents import *
from pygame.locals import *
import sys

def main(agent="manual", pprint=True, trials=1, fn="MaxTile"):

	# Dimensions of 2048 Screen
	XDIM = 600
	YDIM = 750

	if agent == "manual":
		manual2048(XDIM, YDIM, pprint)

	else:
		AI2048(XDIM, YDIM, pprint=pprint, trials=trials, agent=agent, fn=fn)


# if python says run, then we should run
if __name__ == '__main__':

	args = sys.argv

	# ensure proper usage
	if len(args) < 2:
		print("""
		Welcome to 2048, AI edition.  \n
		To run, please retype the following in the command prompt: \n
		python main.py [agent] [flags] \n 
		For more help, use the flag -h.
		""")
		sys.exit()

	if "-h" in args:
		print("""
		To use: python main.py [agent] [flags] \n
		[agent]: manual - allows the user to manually play a game of 2048. \n
		         random - runs a randomized AI agent. \n
		         heuristic - runs an AI agent with a heuristic function. \n
		         expectimax - runs Expectimax AI agent
		[flags]: -p - runs the game with graphics and a display board \n
		         -h - opens the help menu.  \n
		         -t - number of games to play.  Ex. python main.py random -t 1000 \n
		         -fn - function to use if agent is heuristic. Note that the \n
		         valid heuristic function are the following:
		         	MaxTile
		         	NumEmpty
		""")
		sys.exit()

	# more than 1 argument provided
	agent = args[1]

	if agent[0] == "-":
		print("""
		Need to provide agent as first optional argument: \n 
		python main.py [agent] [flags]
		""")

	# initialize argument values
	tArg, pArg, fnArg = False, False, None

	for i, arg in enumerate(args):
		if arg == "-t" and i < len(args) - 1:
			if args[i + 1].isdigit():
				tArg = True
				tArgVal = int(args[i + 1])
		if arg == "-p":
			pArg = True
		if arg == "-fn" and i < len(args) - 1:
			fnArg = args[i + 1]

	if tArg:
		main(agent=agent, pprint=pArg, trials=tArgVal, fn=fnArg)
	else:
		main(agent=agent, pprint=pArg, trials=1, fn=fnArg)
