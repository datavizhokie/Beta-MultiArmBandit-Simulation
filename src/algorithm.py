
from matplotlib import pyplot as plt
from prior import create_priors

class Algorithm:
    def __init__(self):
        pass
    def update(self):
        pass
    def plot(self):
        pass
    def export(self):
        pass
    def allocate(self):
        pass


class BayesianAlgorithm(Algorithm):
    def __init__(self, experiment_config, allocator):
        self.priors = create_priors(
            arm_names=experiment_config.get_variant_uuids(),
            metric_names=experiment_config.get_metric_names(),
            metric_types=['beta', 'gaussian']
        )
        self.allocator = allocator

    def update(self, payoffs):
        self.priors.update(payoffs)

    def allocate(self, allocations):
        self.allocator.set_assignments(self.priors, allocations)

    def plot(self, filename):
        self.priors.plot()
        plt.savefig(filename)
        plt.close()


class UniformAlgorithm(Algorithm):
    def __init__(self, experiment_config, allocator):
        pass
    def update(self, payoffs):
        pass
    def allocate(self, allocations):
        # TODO: implement
        pass