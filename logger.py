# logger.py
# ---------------
# Contains methods to collect turn-by-turn game state data
# and add the data to a CSV file with the current datetime
# as its title. 

from gameObjects import *
import datetime

def beginLog(state):
	"""
	Creates a .csv file to write data to.  The headers
	will be the following:
	Val0, Val1, ..., Val15, Score, Time, Agent, AgentHeur, Move, Trial
	"""
	numVals = state.size * state.size
	currtime = datetime.datetime.now()
	date = repr(currtime.day) + "-" + repr(currtime.hour) + "-" + \
		   repr(currtime.minute) + "-" + repr(currtime.second)
	fname = "logs/" + date + "-" + "2048-log.csv"
	f = open(fname, "w+")

	for i in range(numVals):
		f.write("Val" + repr(i) + ",")

	f.write("Score,Time,Agent,AgentHeur,Move,Trial,RandTilePos\n")

	f.close()

	return fname

def log(fileName, state, time, agent, move, trial):

	f = open(fileName, "a")

	values = ""
	for i in range(state.size):
		for j in range(state.size):
			values += repr(state.grid[i][j]) + ","

	score = state.score

	f.write(values + repr(score) + "," + repr(time) + "," + type(agent).__name__ + ",N/A," + move + \
		    "," + repr(trial) + "," + repr(state.mostRecentRandomTilePos[0] * state.size + state.mostRecentRandomTilePos[1]) + "\n")

	f.close()
