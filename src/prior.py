import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta as beta_distribution


class BetaPrior:
    def __init__(self, arm, metric):
        self.a = 1.0
        self.b = 1.0
        self.arm = arm
        self.metric = metric

    def update(self, payoffs):
        self.a += payoffs['num-success']
        self.b += payoffs['num-trials'] - payoffs['num-success']

    def update_stats(self):
        return [
            'num-trials',
            'num-successes'
        ]
    def sample(self):
        return np.random.beta(a=self.a, b=self.b)

    def plot(self, t):
        b = beta_distribution(self.a, self.b)
        plt.plot(
            t,
            b.pdf(t),
            label=r'Arm=%s, Metric=%s \alpha=%.1f, \beta=%.1f$' % (self.arm, self.metric, self.a, self.b)
        )

class GaussianPrior:
    def __init__(self, arm, metric):
        self.mean = 0
        self.variance = 1
        self.arm = arm
        self.metric = metric

    def update(self, experiment_payoffs):
        pass

    def update_stats(self):
        return [
            'count',
            'mean',
            'variance'
        ]

    def sample(self):
        return np.random.normal(loc=self.mean, scale=self.variance)

    def plot(self, t):
        pass


class Priors:
    # ugly
    def __init__(self, arm_names, metric_names, distributions):
        self.arm_names = arm_names
        self.metric_names = metric_names
        self.distributions = distributions

    def get_arm_names(self):
        return self.arm_names

    def get_metric_names(self):
        return self.metric_names

    def update(self, bandit_payoffs):
        for arm_name in self.distributions.keys():
            arm_dists = self.distributions[arm_name]
            for metric_name in arm_dists.keys():
                dist = arm_dists[metric_name]
                if arm_name not in bandit_payoffs:
                    continue
                if metric_name not in bandit_payoffs[arm_name]:
                    continue
                dist.update(bandit_payoffs[arm_name][metric_name])

    def sample(self, arm, metric):
        return self.distributions[arm][metric].sample()

    def plot(self):
        t = np.linspace(0, 1, 1000)
        for arm in self.distributions.values():
            for prior in arm.values():
                prior.plot(t)

def create_priors(arm_names, metric_names, metric_types):
    distributions = {}
    for arm_name in arm_names:
        arm_dists = {}
        distributions[arm_name] = arm_dists
        for metric_name, metric_type in zip(metric_names, metric_types):
            if metric_type == 'beta':
                arm_dists[metric_name] = BetaPrior(arm_name, metric_name)
            elif metric_type == 'gaussian':
                arm_dists[metric_name] = GaussianPrior(arm_name, metric_name)
            else:
                raise Exception("Unknown metric type: " + metric_type)
    return Priors(arm_names, metric_names, distributions)
