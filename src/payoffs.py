from enum import Enum
import numpy as np
import json

def get_metric_names(variant_metric_values):
    return list(set([
        metric_name
        for variant in variant_metric_values.values()
        for metric_name in variant.keys()
    ]))

#def only_has_one_metric(variant_metric_values):
#    return np.all(map(lambda v: len(v.keys()) == 1, variant_metric_values.values()))

def determine_winner(variant_metric_values):
    metric_names = get_metric_names(variant_metric_values)
    if len(metric_names) == 1:
        metric_name = metric_names[0]
        max_variant = max(variant_metric_values.keys(), key=lambda v: variant_metric_values[v][metric_name])
        return max_variant

    print(variant_metric_values)
    # compare safety metrics
    # compare each level of metric
    # return the winner
    return np.random.choice([key for key in variant_metric_values.keys()])

class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    NONE = 'none'

class Metric:
    def __init__(self, name):
        self.name = name
        self.circuit_breaker = False  # isSafetyMetric
        self.priority = 0  # the order to compare them
        self.success = False
        self.direction = Direction.NONE
        self.values = []

class BanditMetrics:
    def __init__(self, bandit_uuid):
        self.metrics = {}
        self.uuid = bandit_uuid

    def get_metric(self, name):
        if name not in self.metrics:
            metric = Metric(name)
            self.metrics[name] = metric
        return self.metrics[name]

    def convert(self, metric_value):
        count = metric_value['count']
        sum = metric_value['sum']
        sumOfSquares = metric_value['sum-of-squares']
        return {
            'num-trials': count,
            'num-success': sum,

            'count': count,
            'mean': sum / count,
            'variance': (count / (count - 1.0)) * (sumOfSquares / count - (sum / count) ** 2)
        }

    def subset(self, day):
        result = {}
        for metric in self.metrics.values():
            for metric_value in metric.values:
                # TODO:
                if day not in metric_value['day']:
                    continue

                if metric_value['variant-uuid'] not in result:
                    result[metric_value['variant-uuid']] = {}
                variant_info = result[metric_value['variant-uuid']]
                variant_info[metric_value['metric-name']] = self.convert(metric_value)
        return result

class Payoffs:
    def __init__(self):
        self.bandits = {}

    def add_bandit_metrics(self, bandit_metrics):
        self.badits[bandit_metrics.uuid] = bandit_metrics

    def get_bandit_payoffs(self, bandit_uuid):
        if bandit_uuid not in self.bandits:
            self.bandits[bandit_uuid] = BanditMetrics(bandit_uuid)
        return self.bandits[bandit_uuid]

def load_payoffs(file, config):
    raw_json = None
    with open(file, "r") as payoff_input:
        raw_json = json.load(payoff_input)

    payoffs = Payoffs()

    for m in raw_json["data"]["allMetricAggregations"]:
        for value in m["rawAggregationEntries"]:
            day = value["aggregationIdentifier"]["for"]
            metric_name = value["aggregationIdentifier"]["metric"]
            variant_uuid = value["aggregationIdentifier"]["variantUuid"]
            count = value["count"]
            sum = value["sum"]
            sum_of_squares = value["sumOfSquares"]

            experiment_uuid = config.get_experiment_for_variant(variant_uuid)

            bandit_metrics = payoffs.get_bandit_payoffs(experiment_uuid)
            metric = bandit_metrics.get_metric(metric_name)
            # verbosity not needed
            metric.values.append({
                'day': day,
                'metric-name': metric_name,
                'variant-uuid': variant_uuid,
                'count': count,
                'sum': sum,
                'sum-of-squares': sum_of_squares
            })

    return payoffs