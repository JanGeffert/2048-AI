# loggingAnalysis.py
# ---------------
# Returns summary visualizations of the gameplay for
# the CSV game log file that is input as a commandline
# argument

import argparse
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

# Input CSV name should be logs/11-15-37-58-2048-log.csv (or similar)
parser = argparse.ArgumentParser(description = "Input CSV file to analyze")
parser.add_argument(dest = "fname", help = "name of CSV file to analyze")
args = parser.parse_args()

data = pd.read_csv(args.fname)
n = 4

num_moves = data.loc[:, "Move"].value_counts()

#### BAR CHART TO OBSERVE MOST COMMON MOVES ####
#
x = range(len(num_moves))
plt.title("Moves Taken Over Course of Trials")
plt.bar(x, num_moves.values, align = 'center', alpha = 0.5)
plt.xticks(x, num_moves.axes[0])
plt.savefig("2048_moves_barchart")
plt.show()

#### HEATMAP TO OBSERVE TILE LOCATION CHANGES OVER TIME ####
#
which_squares_occupied = data.loc[:, "Val0":"Val15"] != 0
sum_tiles_is_occupied = np.array(which_squares_occupied.sum()).reshape((n, n))

sns.heatmap(
    sum_tiles_is_occupied,
    cmap = "Blues",
    annot = sum_tiles_is_occupied
)
plt.title("Squares Most Often Populated")
plt.axis("off")
plt.savefig("2048_tile_heatmap")
plt.show()

#### PLOT TO OBSERVE MEAN SCORE AND SPREAD ACROSS TRIALS ####
#
score_trial_pair_data = data.loc[:, ["Score", "Trial"]]
trials = np.unique(score_trial_pair_data.Trial)

# List to contain each trial's score series
scores_lst_by_trial = []
for trial_num in trials:
    indices_of_trial = score_trial_pair_data["Trial"] == trial_num
    trial_data = score_trial_pair_data.loc[indices_of_trial].reset_index(drop = True)
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
plt.savefig("2048_score_and_spread")
plt.show()

#### HEATMAP TO OBSERVE MOST COMMON LOCATION OF MAXTILE ####
tiles = data.loc[:, "Val0":"Val15"].copy()

# True for entry within particular row if that entry contains max tile value
# at that point in the game, otherwise false
is_max_tile_each_row = tiles.apply(
    lambda row: row == data.loc[:, "Val0":"Val15"].max(axis = 1)
)

frequency_max_tile = np.array(is_max_tile_each_row.sum()).reshape((n, n))

sns.heatmap(
    frequency_max_tile,
    cmap = "Blues",
    annot = frequency_max_tile
)
plt.title("Squares Most Often Populated by Max Tile")
plt.axis("off")
plt.savefig("2048_max_tile_heatmap")
plt.show()


#### MOVES REQUIRED TO REACH EACH TILE OVER COURSE OF EACH TRIAL ####
#
tiles = data.loc[:, "Val0":"Val15"].copy()

# Entry in this list is list of attained values over a particular trial
# in ascending order
unique_maxes_over_all_trials = []

# Entry in this list is list of number of moves required to reach each
# of the attained values in corresponding list in unique_maxes_over_all_trials
num_moves_required_over_all_trials = []

for trial in trials:
    # Subset data to relevant trial
    indices_of_trial = data["Trial"] == trial
    trial_tiles = tiles.loc[indices_of_trial].reset_index(drop = True)

    max_at_each_move = trial_tiles.max(axis = 1)

    # The highest vals reached across entire trial
    unique_maxes = np.unique(max_at_each_move)
    unique_maxes_over_all_trials.append(list(unique_maxes))

    # Get index of first appearance of particular max tile
    # over course of a trial, corresponds to number of moves needed
    # to reach that tile
    num_moves_required = [max_at_each_move[max_at_each_move == tile].index[0] for tile in unique_maxes]
    num_moves_required_over_all_trials.append(num_moves_required)

def return_longest_sublist(lst):
    return max(lst, key = len)

best_trial_maxes = return_longest_sublist(unique_maxes_over_all_trials)
best_trial_num_moves = return_longest_sublist(num_moves_required_over_all_trials)

plt.plot(best_trial_num_moves, best_trial_maxes)
plt.title("Number Moves Required to Reach Each Tile\n(For the best trial)")
plt.yscale('log', basey = 2)
plt.xscale('log', basex = 2)
plt.xlabel("Number of Moves")
plt.ylabel("Tile Value Reached")
plt.yticks(best_trial_maxes)
plt.grid(axis = 'y')
plt.savefig("2048_num_moves_required")
plt.show()

##### ADJACENT DIFFERENCES ACROSS ALL TRIALS ####
#
# Input is row representing game state
# Outputs all of the adjacent tile differences as a list
# Does not count differences between tile and empty square
# or differences between empty squares
def get_relevant_diffs(row):
    board = row.values.reshape(n, n)
    board = board.astype("float")
    board[board == 0] = np.NaN

    board_diff_vert = np.diff(board, axis = 0); vflat = board_diff_vert.flatten()
    board_diff_horz = np.diff(board, axis = 1); hflat = board_diff_horz.flatten()

    vdiffs = [int(abs(elt)) for elt in vflat if not np.isnan(elt)]
    hdiffs = [int(abs(elt)) for elt in hflat if not np.isnan(elt)]

    vdiffs.extend(hdiffs)

    return vdiffs

all_diffs_across_game = []
for index, row in tiles.iterrows():
    all_diffs_across_game.extend(get_relevant_diffs(row))

plt.hist(all_diffs_across_game)
plt.title("Differences Between Adjacent Tiles \nAcross all Trials")
plt.xlabel("Adjacent Differences")
plt.savefig("2048_adjacent_diffs")
plt.show()

def get_score_summary(data):
    scores_list = []
    for trial in trials:
        trial_subset = data.loc[data["Trial"] == trial, :]
        final_score = trial_subset.tail(1)["Score"]
        scores_list.append(int(final_score))
    return np.mean(scores_list), np.std(scores_list)

print(get_score_summary(data))
