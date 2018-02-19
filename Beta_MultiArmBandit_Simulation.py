import numpy as np
from numpy import *
from scipy.stats import beta
import random
import timeit
import pandas as pd
import sys
from matplotlib import pyplot as plt

start = timeit.default_timer()

class BetaBandit(object):
    def __init__(self, num_options=4, prior=(1.0,1.0)):
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


def boolean_select(self):
    theta_random = (random.random(),random.random(),random.random(),random.random())
    if random.random() > theta_random[choice]:
        return True
    else:
        return False


N = 5000
trials = zeros(shape=(N,4))
successes = zeros(shape=(N,4))
beta_full_frame = []
theta_full_frame = []
choices = []

bb = BetaBandit()

for i in range(N):
    global increment
    increment = i
    choice = bb.get_recommendation()
    beta_full_frame.append(beta_params_frame)
    theta_full_frame.append(sampled_theta_frame)
    choice_and_event =[i, choice]
    choices.append(choice_and_event)
    # Increment chosen arm for ith event... [i:choice]
    trials[i:choice] = trials[i:choice]+1
    conv = boolean_select(choice)
    bb.add_result(choice, conv)
    trials[i] = bb.trials
    successes[i] = bb.successes

theta_temp= pd.concat(theta_full_frame, axis=0)
theta_df = pd.DataFrame(theta_temp)

theta_df = theta_df.reset_index(inplace=False)

theta_df['Event'] = theta_df.index
print(theta_df)

# Transpose various data sources for final joins
theta_df_trans =pd.melt(theta_df, id_vars='Event', value_vars=[0, 1, 2, 3], value_name='Sample_Theta')
theta_df_trans = theta_df_trans.rename(columns={'variable': 'Arm'})

trials_df = pd.DataFrame(trials, columns =['Arm0','Arm1','Arm2','Arm3'])
trials_df['Event'] = trials_df.index
choice_df = pd.DataFrame(choices, columns=['Event','Choice'])

beta_temp= pd.concat(beta_full_frame, axis=0)
beta_df = pd.DataFrame(beta_temp, columns=['Arm', 'a', 'b','Event'])

beta_full_df = pd.merge(beta_df, choice_df[['Event','Choice']], on=['Event'], how='left')
# Merge each choice per event to the beta data
beta_merge1 = pd.merge(beta_full_df, trials_df[['Event','Arm0','Arm1','Arm2','Arm3']], on=['Event'], how='left')
# Merge max sampled theta values to each event
beta_final = pd.merge(beta_merge1, theta_df_trans[['Event','Arm','Sample_Theta']], on=['Event','Arm'], how='left')

beta_final.to_csv('Beta Distribution Data.csv', index=False)

from pylab import *
subplot(211)
n = arange(N)+1
plot(n, trials[:,0], label="Arm 0 - Vice Principals")
plot(n, trials[:,1], label="Arm 1 - Young Pope")
plot(n, trials[:,2], label="Arm 2 - The Deuce")
plot(n, trials[:,3], label="Arm 3 - GoT")
legend()
title('Theoretical HBO Shows - Successes per Arm (%i Simulated Events)' % N)
xlabel("Number of trials")
ylabel("Successes")

legend()
show()

stop = timeit.default_timer()
print("Total Seconds Elapsed:", stop - start)