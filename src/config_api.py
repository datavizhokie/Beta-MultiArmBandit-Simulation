
import json

class ConfigApiExperiment:
    def __init__(self, raw_json):
        self.raw_json = raw_json

    def get_uuid(self):
        return self.raw_json["uuid"]

    def get_name(self):
        return self.raw_json["name"]

    def get_variant_uuids(self):
        return [
            variant["uuid"]
            for variant in self.raw_json["variants"]
        ]

    def get_metric_names(self):
        return [
            metric["name"]
            for metric in self.raw_json["combinedMetrics"]
        ]

    def get_arms(self):
        return self.raw_json["variants"]

class ConfigApiConfig:
    def __init__(self, raw_json):
        self.experiments = {
            experiment["uuid"]: ConfigApiExperiment(experiment)
            for experiment in raw_json["data"]["experiments"]
        }
    def get_experiment_for_variant(self, variant_uuid):
        for experiment in self.experiments.values():
            for variant in experiment.get_variant_uuids():
                if variant == variant_uuid:
                    return experiment.get_uuid()
        raise Exception("Variant not found: " + variant_uuid)

    def get_bandits(self):
        return self.experiments.values()


def load_config(file):
    with open(file, "r") as payoff_input:
        return ConfigApiConfig(json.load(payoff_input))