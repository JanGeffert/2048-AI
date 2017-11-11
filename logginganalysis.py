import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Input CSV name should be logs/11-15-37-58-2048-log.csv (or similar)
parser = argparse.ArgumentParser(description = "Input CSV file to analyze")
parser.add_argument(dest = "fname", help = "name of CSV file to analyze")
# parser.add_argument("--fname", dest = "fname", help = "name of CSV file to analyze")
args = parser.parse_args()

data = pd.read_csv(args.fname)

# fname = sys.argv[1]
# data = pd.read_csv(fname)

# This is hardcoded for 4 x 4 board right now
square_vals = np.array((data.loc[:, "Val0":"Val15"] != 0).sum()).reshape((4, 4))
sns.heatmap(square_vals, cmap = "Blues", annot = a)
plt.show()

plt.plot(range(len(data)), data.loc[:, "Score"])
plt.show()

# print(data.columns.values)