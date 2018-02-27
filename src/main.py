
from algorithm import BayesianAlgorithm
from allocations import create_allocations
from allocator import ThompsonAllocator
from payoffs import load_payoffs
from config_api import load_config
import pandas as pd


config = load_config('data/config.json')
payoffs = load_payoffs('data/analysis.json', config)

dates = [
    date.strftime("%Y-%m-%d")
    for date in pd.date_range(
        "2018-02-01",
        "2018-03-01"
    )
]

algorithms = {
    bandit.get_uuid(): BayesianAlgorithm(bandit, ThompsonAllocator())
    for bandit in config.get_bandits()
}

#TODO: Use the history object
for day in dates:
    allocations = create_allocations(config)
    for bandit in config.get_bandits():
        uuid = bandit.get_uuid()
        algorithm = algorithms[uuid]
        day_payoff = payoffs.get_bandit_payoffs(uuid).subset(day)
        algorithm.update(day_payoff)
        algorithm.allocate(allocations.get_bandit_allocation(uuid))

        algorithm.plot('images/after_' + day + '.png')
    print(allocations.export())
