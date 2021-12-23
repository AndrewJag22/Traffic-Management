# -*- coding: utf-8 -*-
import random
import numpy as np
import networkx as nx


class RSU:
    def __init__(self, road_index, x, alg, sim):
        self.road_index = road_index
        self.x = x
        self.range = 10
        self.sim = sim
        self.active = False
        self.alg = alg

    def update(self, vehicle):
        if vehicle.updated:
            return

        if self.alg == 'density_greedy':
            if vehicle.end != self.road_index:
                current_node = self.sim.edge2nodes[self.road_index][1]
                end_node = self.sim.edge2nodes[vehicle.end][1]
                neighbors = [node for node in self.sim.G.neighbors(current_node)]
                random.shuffle(neighbors)
                distances = [nx.shortest_path_length(self.sim.G, node, end_node, weight='weight') for node in neighbors]
                densities = [self.sim.roads[self.sim.nodes2edge[(current_node, node)][0]].density for node in neighbors]
                scores = [distances[i] + densities[i] * 1.5 for i in range(len(neighbors))]
                next_node = neighbors[np.argmin(scores)]
                new_road = self.sim.nodes2edge[(current_node, next_node)][0]
                vehicle.path += self.sim.curve(self.road_index, new_road)
                vehicle.path.append(new_road)

        elif self.alg == 'density_dijkstra':
            if vehicle.end != self.road_index:
                current_node = self.sim.edge2nodes[self.road_index][1]
                end_node = self.sim.edge2nodes[vehicle.end][1]
                paths = [p for p in nx.all_shortest_paths(self.sim.denseG, current_node, end_node, weight='weight')]
                path = random.choice(paths)
                new_road = self.sim.nodes2edge[(path[0], path[1])][0]
                vehicle.path += self.sim.curve(self.road_index, new_road)
                vehicle.path.append(new_road)

        vehicle.updated = True
