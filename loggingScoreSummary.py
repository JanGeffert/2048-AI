import argparse
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

# Input CSV name should be logs/11-15-37-58-2048-log.csv (or similar)
parser = argparse.ArgumentParser(description = "Input CSV file to analyze")
parser.add_argument(dest = "fname", help = "name of CSV file to analyze")
# parser.add_argument("--fname", dest = "fname", help = "name of CSV file to analyze")
args = parser.parse_args()

data = pd.read_csv(args.fname)

score_trial_pair_data = data.loc[:, ["Score", "Trial"]]
trials = np.unique(score_trial_pair_data.Trial)

def get_score_summary(data):
    scores_list = []
    for trial in trials:
        trial_subset = data.loc[data["Trial"] == trial, :]
        final_score = trial_subset.tail(1)["Score"]
        scores_list.append(int(final_score))


    plt.plot(scores_list)
    plt.show()
    return np.mean(scores_list), np.std(scores_list)

print(get_score_summary(data))
