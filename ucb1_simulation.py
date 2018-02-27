## Source:   https://github.com/j2kun/ucb1/blob/master/ucb1.py
import math
import random
from matplotlib import pyplot as plt
from numpy import *
import numpy as np
import sys
import pandas as pd


# Test UCB1 using stochastic payoffs
num_bandits = 4
numRounds = 100

def __init__(self, num_options=num_bandits):
    self.trials = zeros(shape=(num_options,), dtype=int)

# upperBound: int, int -> float
# the size of the upper confidence bound for ucb1
def upperBound(step, numPlays):
   return math.sqrt(2 * math.log(step + 1) / numPlays)

# ucb1: int, (int, int -> float) -> generator
# perform the ucb1 bandit learning algorithm.  num_bandits is the number of
# actions, indexed from 0. reward is a function (or callable) accepting as
# input the action and producing as output the reward for that action

numPlays_array = np.zeros(shape= (1,4))
def ucb1(num_bandits, reward):
    global numPlays_array
    payoffSums = [0] * num_bandits
    numPlays = [1] * num_bandits
    ucbs = [0] * num_bandits

    #numPlays_array = np.array([numRounds,num_bandits])

    #initialize empirical sums
    for t in range(num_bandits):
        payoffSums[t] = reward(t,t)
        yield t, payoffSums[t], ucbs

    t = num_bandits

    while True:
        ucbs = [payoffSums[i] / numPlays[i] + upperBound(t, numPlays[i]) for i in range(num_bandits)]
        action = max(range(num_bandits), key=lambda i: ucbs[i])

        theReward = reward(action, t)
        numPlays[action] += 1
        numPlays_a = array(numPlays)
        numPlays_a.reshape((1, 4))
        #print(numPlays_a)
        #print(numPlays_array)
        #sys.exit()
        numPlays_array = np.append(numPlays_array, numPlays_a)
        #numPlays_array.append(numPlays)

        payoffSums[action] += theReward

        yield action, theReward, ucbs
        t = t + 1


def add_result(self, trial_id):
    self.trials[trial_id] = self.trials[trial_id] + 1
    #if (reward):
        #self.successes[trial_id] = self.successes[trial_id] + 1


biases = [1.0 / k for k in range(5,5+num_bandits)]
means = [0.5 + b for b in biases]
deltas = [means[0] - x for x in means[1:]]
deltaSum = sum(deltas)
invDeltaSum = sum(1/x for x in deltas)

bestAction = 0
rewards = lambda choice, t: random.random() + biases[choice]

cumulativeReward = 0
bestActionCumulativeReward = 0

regret_list =[]
regretBound_list=[]
t_list=[]
choice_list=[]

numPlays_list = []
successes = zeros(shape=(numRounds,num_bandits))

t = num_bandits
trial_id = 0

for (choice, reward, ucbs) in ucb1(num_bandits, rewards):
    cumulativeReward += reward
    bestActionCumulativeReward += reward if choice == bestAction else rewards(bestAction, t)
    regret = bestActionCumulativeReward - cumulativeReward
    regret_list.append(regret)
    regretBound = 8 * math.log(t + 5) * invDeltaSum + (1 + math.pi*math.pi / 3) * deltaSum
    regretBound_list.append(regretBound)
    choice_list.append(choice)
    #numPlays_list.append(numplays_df)
    # Increment chosen arm for ith event... [t:choice]
    t += 1

    #print("regret: %d\tregretBound: %.2f" % (regret, regretBound))
    t_list.append(t)
    if t >= numRounds:
        break

#numPlays_array.reshape((100, 4))
print(numPlays_array)

sys.exit()



ax1 = plt.subplot(111)
plt.ylabel('Cumulative Regret')
ax1.plot(t_list, regret_list)
ax1.plot(t_list, regretBound_list)
plt.title('UCB1 Regret')
plt.show()


from pylab import *
subplot(211)
n = arange(numRounds)+1

for k in range(num_bandits):
    plot(n, numPlays[:, k], label="Arm %d" % k)

legend()
title('Simulated Allocations per Arm (%i Simulated Events)' % N)
xlabel("Number of Events")
ylabel("Allocations")

legend()
show()