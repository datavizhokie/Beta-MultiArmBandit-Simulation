
import json

class BanditAllocation:
    def __init__(self, config):
        self.info = {
            'arms': {
                arm['uuid']: {
                    'allocation': 0.0,
                    'uuid': arm['uuid'],
                    'name': arm['name']
                }
                for arm in config.get_arms()
            },
            'name': config.get_name(),
            'uuid': config.get_uuid()
        }
        self.metric_names = config.get_metric_names()

    def get_arm(self, arm_uuid):
        return self.info['arms'][arm_uuid]

    def set_arm_allocation(self, arm_uuid, allocation):
        self.get_arm(arm_uuid)['allocation'] = allocation

    def get_arm_allocation(self, arm_uuid):
        return self.get_arm(arm_uuid)['allocation']

    def get_arm_uuids(self):
        return [
            arm['uuid']
            for arm in self.info['arms'].values()
        ]
    def get_metric_names(self):
        return self.metric_names


class Allocations:
    def __init__(self):
        self.bandit_allocations = {}

    def create_bandit_allocation(self, config):
        bandit = BanditAllocation(config)
        self.bandit_allocations[config.get_uuid()] = bandit
        return bandit

    def get_bandit_allocation(self, bandit_uuid):
        return self.bandit_allocations[bandit_uuid]


    def export(self):
        return json.dumps({
            ba.info['uuid']: ba.info
            for ba in self.bandit_allocations.values()
        }, sort_keys=True, indent=2, separators=(",", ": "))

def create_allocations(config):
    allocations = Allocations()
    for bandit in config.get_bandits():
        allocations.create_bandit_allocation(bandit)
    return allocations