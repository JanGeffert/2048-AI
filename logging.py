from gameObjects import *
import time

def beginLog(state):
	""" 
	Creates a .csv file to write data to.  The headers
	will be the following:
	Val0, Val1, ..., Val15, Score, Agent, AgentHeur, Move
	"""
	numVals = state.size * state.size
	date = repr(time.gmtime())
	fname = date + "-" + "2048-log.csv"
	f = open(fname, "w+")

	for i in range(len(numVals)):



