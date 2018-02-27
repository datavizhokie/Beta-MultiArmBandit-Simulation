
from payoffs import determine_winner

class Allocator:
    def __init__(self):
        pass
    def set_assignments(self, priors, bandit_allocations):
        pass

class ThompsonAllocator:
    def __init__(self, number_of_samples=1000):
        self.num_samples = number_of_samples

    def set_assignments(self, priors, bandit_allocations):
        metric_names = bandit_allocations.get_metric_names()
        arm_uuids = bandit_allocations.get_arm_uuids()

        arm_values = {
            arm_name: {
                'number_wins': 0
            }
            for arm_name in arm_uuids
        }

        for _ in range(self.num_samples):
            winner = determine_winner({
                arm_uuid: {
                    metric: priors.sample(arm_uuid, metric)
                    for metric in metric_names
                }
                for arm_uuid in arm_uuids
            })
            arm_values[winner]['number_wins'] += 1

        for arm_uuid in arm_uuids:
            # This is the estimated probability that this variant is the winner
            p = arm_values[arm_uuid]['number_wins'] / float(self.num_samples)
            bandit_allocations.set_arm_allocation(arm_uuid, p)



class ConservativeAllocator:
    def __init__(self, delegate):
        self.delegate_sampler = delegate
        self.gamma = 1

    def scale_towards_uniform(self, num_arms, assignment):
        uniform_assignment = 1 / float(num_arms)
        return uniform_assignment + self.gamma * (assignment - uniform_assignment)

    def set_assignments(self, priors, bandit_allocations):
        arm_uuids = bandit_allocations.get_arm_uuids()
        num_arms = len(arm_uuids)

        self.delegate_sampler.set_assignments(priors, bandit_allocations)

        prev_assignments = {
            variant_uuid: bandit_allocations.get_arm_allocation(variant_uuid)
            for variant_uuid in arm_uuids
        }

        scaled_assignments = {
            variant_uuid: self.scale_towards_uniform(num_arms, prev_assignments[variant_uuid])
            for variant_uuid in arm_uuids
        }

        total_allocation = sum(scaled_assignments.values())

        normalized_assignments = {
            variant_uuid: scaled_assignments[variant_uuid] / total_allocation
            for variant_uuid in arm_uuids
        }

        for variant_uuid in arm_uuids:
            bandit_allocations.set_arm_allocation(
                variant_uuid,
                normalized_assignments[variant_uuid]
            )