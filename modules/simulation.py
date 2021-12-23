# -*- coding: utf-8 -*-
import random
import networkx as nx

from copy import deepcopy
from modules.road import Road
from modules.traffic_sign import TrafficSign


class Simulation:
    def __init__(self):
        self.road_index = 0
        self.dt = 1 / 60
        self.t = 0.0
        self.frames = 0
        self.roads = []
        self.schedule = None
        self.G = None
        self.nodes2edge = None
        self.edge2nodes = None
        self.traffic_signs = []
        self.curve = None
        self.arrived = 0
        self.elapsed = 0
        self.denseG = None
        self.straight = 0
        self.no_rsu = True
        self.max_traffic = 0

    def create_road(self, start, end):
        road = Road(self.road_index, start, end)
        self.roads.append(road)
        self.road_index += 1

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def create_sign(self, roads):
        roads = [[self.roads[i] for i in road_group] for road_group in roads]
        sign = TrafficSign(roads, len(roads))
        self.traffic_signs.append(sign)

    def create_schedule(self, schedule):
        self.schedule = schedule

    def create_graph(self, G, nodes2edge, edge2nodes, curve):
        self.G = G
        self.nodes2edge = nodes2edge
        self.edge2nodes = edge2nodes
        self.curve = curve
        self.denseG = G.copy()

    def use_rsu(self):
        self.no_rsu = False

    def update(self):
        for road in self.roads:
            road.update(self.dt)
            if self.max_traffic < len(road.vehicles):
                self.max_traffic = len(road.vehicles)

        # update denseG
        self.denseG = self.G.copy()
        for road_index in range(self.straight):
            road = self.roads[road_index]
            edge = self.edge2nodes[road_index]
            self.denseG.edges[edge]['weight'] = max(self.G.edges[edge]['weight'], (road.density + 1) * 0.8)

        if self.schedule and len(self.schedule) != 0:
            time, vehicles = next(iter(self.schedule.items()))
            if time <= self.t:
                del self.schedule[time]
                for vehicle in vehicles:
                    self.roads[vehicle.start].vehicles.append(vehicle)

        for sign in self.traffic_signs:
            sign.update(self)

        for road_index in range(len(self.roads)):
            road = self.roads[road_index]
            if len(road.vehicles) == 0:
                continue

            vehicle = road.vehicles[0]
            if vehicle.x >= road.length:
                if vehicle.end == road_index:
                    self.elapsed += vehicle.t
                    self.arrived += 1

                if vehicle.current_road_index + 1 < len(vehicle.path):
                    vehicle.current_road_index += 1
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    new_vehicle.updated = False
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(new_vehicle)
                road.vehicles.popleft()

        if self.no_rsu:
            for road_index in range(len(self.roads)):
                for vehicle in self.roads[road_index].vehicles:
                    if vehicle.path[-1] == road_index and vehicle.end != road_index:
                        current_node = self.edge2nodes[road_index][1]
                        end_node = self.edge2nodes[vehicle.end][1]
                        paths = [p for p in nx.all_shortest_paths(self.G, current_node, end_node, weight='weight')]
                        path = random.choice(paths)
                        new_road = self.nodes2edge[(path[0], path[1])][0]
                        vehicle.path += self.curve(road_index, new_road)
                        vehicle.path.append(new_road)

        for road_index in range(self.straight):
            road = self.roads[road_index]
            if road.rsu:
                road.rsu.active = False
                for vehicle in road.vehicles:
                    if abs(vehicle.x - road.rsu.x) <= road.rsu.range:
                        road.rsu.active = True
                        road.rsu.update(vehicle)

        self.t += self.dt
        self.frames += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
