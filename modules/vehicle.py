# -*- coding: utf-8 -*-
import numpy as np


class Vehicle:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = 4
        self.s0 = 4
        self.T = 1
        self.v_max = 8.3
        self.a_max = 1.44
        self.b_max = 4.61
        self.path = [start]
        self.current_road_index = 0
        self.x = 0
        self.v = self.v_max
        self.a = 0
        self.stopped = False
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self._v_max = self.v_max
        self.t = 0
        self.updated = False

    def update(self, lead, dt):
        if self.v + self.a * dt < 0:
            self.x -= 0.5 * (self.v ** 2) / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * (dt ** 2) / 2

        alpha = 0
        if lead:
            dx = lead.x - self.x - lead.length
            dv = self.v - lead.v
            alpha = (self.s0 + max(0, self.v * (self.T + dv / self.sqrt_ab))) / dx
        self.a = self.a_max * (1 - (self.v / self.v_max) ** 4 - alpha ** 2)

        if self.stopped:
            self.a = -self.b_max * self.v / self.v_max
        self.t += dt

    def stop(self):
        self.stopped = True

    def unstop(self):
        self.stopped = False

    def slow(self, v):
        self.v_max = v

    def unslow(self):
        self.v_max = self._v_max
