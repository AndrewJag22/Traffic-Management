# -*- coding: utf-8 -*-
from collections import deque
from scipy.spatial import distance
from modules.rsu import RSU


class Road:
    def __init__(self, road_index, start, end):
        self.road_index = road_index
        self.start = start
        self.end = end
        self.vehicles = deque()
        self.rsu = None

        self.length = distance.euclidean(start, end)
        self.sin = (end[1] - start[1]) / self.length
        self.cos = (end[0] - start[0]) / self.length
        self.traffic_sign = None
        self.traffic_sign_group = None
        self.has_traffic_sign = False
        self.density = 0.0

    def create_rsu(self, alg, sim):
        self.rsu = RSU(self.road_index, 0.7 * self.length, alg, sim)

    def set_traffic_sign(self, sign, group):
        self.traffic_sign = sign
        self.traffic_sign_group = group
        self.has_traffic_sign = True

    @property
    def traffic_sign_state(self):
        if self.has_traffic_sign:
            group = self.traffic_sign_group
            return self.traffic_sign.current_cycle[group]
        return True

    def update(self, dt):
        n_vehicles = len(self.vehicles)
        if n_vehicles > 0:
            self.vehicles[0].update(None, dt)
            for i in range(1, n_vehicles):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, dt)

            if self.traffic_sign_state:
                self.vehicles[0].unstop()
                for vehicle in self.vehicles:
                    vehicle.unslow()
            else:
                if self.vehicles[0].x >= self.length - self.traffic_sign.slow_distance:
                    slow_v = self.traffic_sign.slow_factor * self.vehicles[0]._v_max
                    self.vehicles[0].slow(slow_v)
                if ((self.vehicles[0].x >= self.length - self.traffic_sign.stop_distance) and
                        (self.vehicles[0].x <= self.length - self.traffic_sign.stop_distance / 2)):
                    self.vehicles[0].stop()
        self.density = n_vehicles // 4
