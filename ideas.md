# Ideas
* Make test board instances to see how our algorithm makes a decision in different cases
  - Can be used to provide visualizations of how an algorithm 'thinks' in different scenarios

# Agents
* Greedy agents with different heuristics
  - Individual heuristics based on metrics below
  - Weighted linear combination of individual heuristics
  - Local search to determine optimal weights
* Expectimax Agent
  - Tune different plys - optimize for both performance and time
  - Use different heuristic functions 
* MDP Agent
  - Derive policies based on current board state and different heuristic functions
* Q-learning agent
* Neural-Nets, Bayesian agents

# Metrics
* Highest Tile Reached
* Total Score at EndGame
* Distribution of Moves Made
* Average number of empty squares
* Distribution of relative location of max tile on board
* Monotonicity - how close together tile values are
* Number of merges per move on average
