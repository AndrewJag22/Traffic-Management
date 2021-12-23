# -*- coding: utf-8 -*-
from itertools import permutations


class TrafficSign:
    def __init__(self, roads, groups):
        self.roads = roads
        self.groups = groups
        self.cycle = [[False] * i + [True] + [False] * (groups - i - 1) for i in range(groups)]
        self.slow_distance = 20
        self.slow_factor = 0.5
        self.stop_distance = 10
        self.current_cycle_index = 0
        self.last_t = 0

        for i in range(len(self.roads)):
            for road in self.roads[i]:
                road.set_traffic_sign(self, i)

    @property
    def current_cycle(self):
        return self.cycle[self.current_cycle_index]

    def update(self, simulation):
        cycle_length = 13
        k = (simulation.t // cycle_length) % self.groups
        self.current_cycle_index = int(k)
