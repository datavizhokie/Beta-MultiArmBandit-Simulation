import numpy as np
from numpy import *
from scipy.stats import beta
import random
import timeit
import pandas as pd
import sys
from matplotlib import pyplot as plt
np.seterr(divide='ignore', invalid='ignore')

start = timeit.default_timer()

#### Simulation Parameters ###
# Number of Bandits supported 3, 4, 5, and 6
num_bandits = 3
N = 50
##############################

class BetaBandit(object):
    def __init__(self, num_options=num_bandits, prior=(1.0,1.0)):
        self.trials = zeros(shape=(num_options,), dtype=int)
        self.successes = zeros(shape=(num_options,), dtype=int)
        self.num_options = num_options
        self.prior = prior

    def add_result(self, trial_id, success):
        self.trials[trial_id] = self.trials[trial_id] + 1
        if (success):
            self.successes[trial_id] = self.successes[trial_id] + 1

    def get_recommendation(self):
        sampled_theta = []
        beta_params = []
        sampled_theta_complete = []
        for i in range(self.num_options):
            global beta_params_frame
            global sampled_theta_frame

            #Construct beta distribution for posterior
            a = self.prior[0] + self.successes[i]
            b = self.prior[1]+ self.trials[i] - self.successes[i]
            dist = beta(self.prior[0] + self.successes[i],
                        self.prior[1]+ self.trials[i] - self.successes[i])

            #Draw sample from beta distribution
            sampled_theta += [ dist.rvs() ]
            beta_params += [{"Arm":i, 'a': a, 'b': b, 'Event' : increment}]
            if i == max(range(self.num_options)):
                sampled_theta_complete+= [sampled_theta]
        beta_params_frame = pd.DataFrame(beta_params)
        sampled_theta_frame = pd.DataFrame(sampled_theta_complete)

        # Return the index of the sample with the largest value
        return sampled_theta.index( max(sampled_theta) )

    def regret(self):
        '''
        Calculate expected regret, where expected regret is
        maximum optimal reward - sum of collected rewards, i.e.
        expected regret = T*max_k(mean_k) - sum_(t=1-->T) (reward_t)
        '''
        return (sum(self.trials)*np.max(np.nan_to_num(self.successes/self.trials)) -
                sum(self.successes)) / sum(self.trials)


def boolean_select(self):
    # Create list of random feedback Theta values, based on the number of specified bandits
    theta_random = []
    for i in range(num_bandits):
        theta_random.append(random.random())
    # Check a random value against the random thetas for each bandit
    if random.random() > theta_random[choice]:
        return True
    else:
        return False


trials = zeros(shape=(N,num_bandits))
successes = zeros(shape=(N,num_bandits))
beta_full_frame = []
theta_full_frame = []
choices = []
regret_list =[]

bb = BetaBandit()

for i in range(N):
    global increment
    increment = i
    choice = bb.get_recommendation()
    beta_full_frame.append(beta_params_frame)
    theta_full_frame.append(sampled_theta_frame)
    choice_and_event =[i, choice]
    choices.append(choice_and_event)
    regret=bb.regret()
    regret_list.append(regret)
    # Increment chosen arm for ith event... [i:choice]
    trials[i:choice] = trials[i:choice]+1
    # Randomly assign if a consumer chooses the recommended content
    conv = boolean_select(choice)
    bb.add_result(choice, conv)
    trials[i] = bb.trials
    successes[i] = bb.successes

theta_temp= pd.concat(theta_full_frame, axis=0)
theta_df = pd.DataFrame(theta_temp)

theta_df = theta_df.reset_index(inplace=False)

theta_df['Event'] = theta_df.index

# Transpose various data sources for final joins
theta_df_trans =pd.melt(theta_df, id_vars='Event',  value_name='Sample_Theta')#, value_vars=[0, 1, 2, 3])
theta_df_trans = theta_df_trans.rename(columns={'variable': 'Arm'})

if num_bandits == 3:
    trials_df = pd.DataFrame(trials, columns=['Arm0', 'Arm1', 'Arm2'])
elif num_bandits == 4:
    trials_df = pd.DataFrame(trials, columns =['Arm0','Arm1','Arm2','Arm3'])
elif num_bandits == 5:
    trials_df = pd.DataFrame(trials, columns =['Arm0','Arm1','Arm2','Arm3','Arm4'])
elif num_bandits == 6:
    trials_df = pd.DataFrame(trials, columns =['Arm0','Arm1','Arm2','Arm3','Arm4','Arm5'])

trials_df['Event'] = trials_df.index

# ADD ALLOCATION OF EACH ARM TO TOTAL NUMBER OF ARMS  - inidividual trial count/sum(trial counts)

choice_df = pd.DataFrame(choices, columns=['Event','Choice'])

beta_temp= pd.concat(beta_full_frame, axis=0)
beta_df = pd.DataFrame(beta_temp, columns=['Arm', 'a', 'b','Event'])

beta_full_df = pd.merge(beta_df, choice_df[['Event','Choice']], on=['Event'], how='left')

# Merge each choice per event to the beta data
if num_bandits == 3:
    beta_merge1 = pd.merge(beta_full_df, trials_df[['Event','Arm0','Arm1','Arm2']], on=['Event'], how='left')
elif num_bandits == 4:
    beta_merge1 = pd.merge(beta_full_df, trials_df[['Event', 'Arm0', 'Arm1', 'Arm2','Arm3']], on=['Event'], how='left')
elif num_bandits == 5:
    beta_merge1 = pd.merge(beta_full_df, trials_df[['Event', 'Arm0', 'Arm1', 'Arm2','Arm3','Arm4']], on=['Event'], how='left')
elif num_bandits == 6:
    beta_merge1 = pd.merge(beta_full_df, trials_df[['Event', 'Arm0', 'Arm1', 'Arm2','Arm3','Arm4','Arm5']], on=['Event'], how='left')

# Merge max sampled theta values to each event
beta_final = pd.merge(beta_merge1, theta_df_trans[['Event','Arm','Sample_Theta']], on=['Event','Arm'], how='left')

beta_final.to_csv('Beta Distribution Data.csv', index=False)

from pylab import *
subplot(211)
n = arange(N)+1

for k in range(num_bandits):
    plot(n, trials[:, k], label="Arm %d" % k)

legend()
title('Simulated Allocations per Arm (%i Simulated Events)' % N)
xlabel("Number of Events")
ylabel("Allocations")

legend()
show()


for k in range(num_bandits):
    plot(n, successes[:, k], label="Arm %d" % k)

legend()
title('Simulated Consumer Choices - Choices per Arm (%i Simulated Events)' % N)
xlabel("Number of Events")
ylabel("Succeses")

legend()
show()


plot(n, regret_list, label="Bayesian Beta Bandit")
legend()
title('Regret: Fraction of payouts lost by using the sequence of pulls vs. the currently best known arm (%i Simulated Events)' % N)
xlabel("Number of trials")
ylabel("Regret")

legend()
show()

stop = timeit.default_timer()
print("Total Seconds Elapsed:", stop - start)