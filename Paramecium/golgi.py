import numpy as np
from itertools import combinations, permutations


class GolgiApparatus:

    Energy = 0
    spark_limit = 0
    starting_pt = []

    def __init__(self, N, depth, start):
        self.Energy = N
        self.spark_limit = depth
        self.starting_pt = start

    def burst(self):
        self.seed = StepSpark(self.Energy)
        self.seed.spark(self.spark_limit)


class StepSpark:
    n_steps = 0
    random_steps = []
    decision_tree = {}

    def __init__(self, N):
        self.n_steps = N

    def spark(self, depth):
        raw_steps = np.random.randint(0, 9, self.n_steps)
        step_tree = {}
        i = 0
        for step in raw_steps:
            possible_steps = []
            seed = np.random.randint(0, 9, depth).flatten()
            for thought in np.unique(seed):
                possible_steps.append(thought)
            # Take Random Step
            self.random_steps.append(step)
            # Other possible branches from current pt
            step_tree[i] = possible_steps
            i += 1
        self.decision_tree = step_tree
