# -*- coding: utf-8 -*-
from collections import OrderedDict

from modules.vehicle import Vehicle
from modules.simulator import Simulator
from modules.simulation import Simulation

from maps import map1
from maps.map1 import curve

# RANDOM SHORTEST PATH


if __name__ == '__main__':
    simulation = Simulation()
    simulation.create_roads(map1.roads)
    simulation.create_roads(map1.curves)
    simulation.straight = 28
    simulation.create_sign([[1, 9, 24, 19, 12, 16, 8, 23],
                            [2, 3, 11, 6, 18, 20, 22, 10],
                            [7, 4, 5, 17, 27, 14, 13, 15]])

    vehicle_schedule = OrderedDict()
    for t in range(0, 500, 10):
        vehicle_schedule[t] = [
            Vehicle(start=1, end=21),
            Vehicle(start=27, end=25),
            Vehicle(start=24, end=26),
            Vehicle(start=20, end=0)
        ]
    simulation.create_schedule(vehicle_schedule)
    simulation.create_graph(map1.road_G, map1.nodes2edge, map1.edge2nodes, curve)

    simulator = Simulator('scenario1', simulation, height=700)
    simulator.zoom = 2.7
    simulator.run(10)
