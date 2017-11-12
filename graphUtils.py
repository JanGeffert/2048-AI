import matplotlib.pyplot as plt
import math
import numpy as np
import datetime

def plotScoresMaxTiles(scores, maxData):
	maxCounts = [0] * 12
	maxLabels = [2 ** i for i in range(1, 13)]
	# Analyze number maxTiles for each value
	for val in maxData:
		index = int(math.log(val, 2))
		maxCounts[index - 1] += 1

	# Display results graphically 
	f1 = plt.figure()
	f2 = plt.figure()

	ax1 = f1.add_subplot(111)
	ax2 = f2.add_subplot(111)

	ax1.hist(scores)
	width = .5
	ax2.bar(np.arange(12), maxCounts, width)
	ax2.set_xticks(np.arange(12))
	ax2.set_xticklabels((maxLabels))

	currtime = datetime.datetime.now()
	date = repr(currtime.day) + "-" + repr(currtime.hour) + "-" + \
		   repr(currtime.minute) + "-" + repr(currtime.second)

	f1.savefig("figures/" + date + "scores.png")
	f2.savefig("figures/" + date + "maxTiles.png")
	