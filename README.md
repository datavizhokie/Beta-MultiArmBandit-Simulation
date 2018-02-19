# Beta-MultiArmBandit-Simulation
 
This code simulates consumer responses to multi-choice situations. Thompson Sampling is used to pull samples from each arm's Beta Distribution (starting with a uniform prior of Beta(1,1)). The max sampled theta inidicates the arm to be rewarded. Bayesian updates are then applied to each bandit distribution. The learning model eventually produces a winning arm over the specified event space.
