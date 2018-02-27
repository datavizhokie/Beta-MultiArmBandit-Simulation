
import json
import pandas as pd
import numpy as np

num_entries = 500

dates = [
    date.strftime("%Y-%m-%d")
    for date in pd.date_range(
        "2018-02-01",
        "2018-03-01"
    )
]
variants = ["v1", "v2", "v3"]

metrics = [{
    'name': 'm1',
    'type': 'brenoulli',
    'params': {
        'v1': 0.5,
        'v2': 0.51,
        'v3': 0.4
    }
#}, {
#    'name': 'm2',
#    'type': 'gaussian',
#    'params': {
#        'v1': {'mean': 0.5, 'variance': 12},
#        'v2': {'mean': 0.4, 'variance': 11}
#    }
}]


results = {
    'data': {
        'allMetricAggregations': []
    }
}

for metric in metrics:
    metricObj = {
        'name': metric['name'],
        'rawAggregationEntries': []
    }
    for variant in variants:
        for day in dates:
            observations = None
            if metric['type'] == 'brenoulli':
                observations = np.asarray(
                    np.random.binomial(
                        1,
                        metric['params'][variant],
                        num_entries
                    ),
                    dtype=np.float64
                )
            if metric['type'] == 'gaussian':
                observations = np.random.normal(
                    loc=metric['params'][variant]['mean'],
                    scale=metric['params'][variant]['variance'],
                    size=num_entries
                )
            metricObj['rawAggregationEntries'].append({
                "aggregationIdentifier": {
                    "metric": metric['name'],
                    "variantUuid": variant,
                    "by": "DAY",
                    "for": day + "T00:00:00Z"
                },
                "count": len(observations),
                "sum": sum(observations),
                "sumOfSquares": sum(observations ** 2)
            })

    results['data']['allMetricAggregations'].append(metricObj)

with open("data/analysis.json", "w") as output:
    json.dump(
        results,
        output,
        sort_keys=True,
        indent=2,
        separators=(",", ": ")
    )