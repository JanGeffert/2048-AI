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

num_moves = data.loc[:, "Move"].value_counts()

# Most common moves
plt.title("Moves Taken Over Course of Trials")
plt.bar(range(len(num_moves)), num_moves.values, align = 'center', alpha = 0.5)
plt.xticks(range(len(num_moves)), num_moves.axes[0])
plt.savefig("moves_barchart")
plt.show()

# Change this to import board.size instead of 4, 4
which_squares_occupied = data.loc[:, "Val0":"Val15"] != 0
sum_tiles_is_occupied = np.array(which_squares_occupied.sum()).reshape((4, 4))

# In case seaborn doesn't work, this plots the same thing
# plt.pcolormesh(np.flip(a, 0), cmap = "Blues")
# plt.show()

sns.heatmap(
    sum_tiles_is_occupied, 
    cmap = "Blues", 
    annot = sum_tiles_is_occupied
)
plt.title("Squares Most Often Populated")
plt.axis("off")
plt.savefig("tile_heatmap")
plt.show()

score_trial_pair_data = data.loc[:, ["Score", "Trial"]]
trials = np.unique(score_trial_pair_data.Trial)

# List to contain each trial's score series 
scores_lst_by_trial = []
for trial_num in trials:
    indices_of_trial = score_trial_pair_data["Trial"] == trial_num
    trial_data = score_trial_pair_data.loc[indices_of_trial].reset_index()
    scores_lst_by_trial.append(trial_data.loc[:, "Score"])

# Truncate each score series to the shortest scores series across
# the trials (by dropping the na's from the entire dataframe)
scores_by_trial = pd.DataFrame(scores_lst_by_trial).dropna(axis = 1)

# Get mean score across all trials for each move
# Get 75th and 25th percentiles across all trials for each move
# to observe spread
mean_line = scores_by_trial.mean()
percentile_75th = scores_by_trial.quantile(0.75)
percentile_25th = scores_by_trial.quantile(0.25)

# Plot spread and mean
x = range(len(mean_line))
plt.title("Mean Score and Score Variation Across Trials")
plt.plot(x, mean_line, color = 'y', label = "Mean Score")
plt.fill_between(
    x, 
    percentile_75th, 
    percentile_25th, 
    label = "75th/25th quantile spread"
)
plt.legend()
plt.savefig("score_and_spread")
plt.show()