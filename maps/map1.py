# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import networkx as nx
from modules.curve import turn_road


TURN_LEFT = 0
TURN_RIGHT = 1

road_a, road_b = 2, 12
road_l = 50
curve_r = 50
nodes = [
    (-5 * road_l, -2 * road_l - road_a),
    (-5 * road_l, -2 * road_l + road_a),
    (-3 * road_l - road_b, -2 * road_l - road_a),
    (-3 * road_l - road_b, -2 * road_l + road_a),
    (-3 * road_l + road_b, -2 * road_l - road_a),
    (-3 * road_l + road_b, -2 * road_l + road_a),
    (-1 * road_l - road_b, -2 * road_l - road_a),
    (-1 * road_l - road_b, -2 * road_l + road_a),
    (-1 * road_l + road_b, -2 * road_l - road_a),
    (-1 * road_l + road_b, -2 * road_l + road_a),
    (3 * road_l - road_b, -2 * road_l - road_a),
    (3 * road_l - road_b, -2 * road_l + road_a),
    (-3 * road_l - road_a, -2 * road_l + road_b),
    (-3 * road_l + road_a, -2 * road_l + road_b),
    (-1 * road_l - road_a, -2 * road_l + road_b),
    (-1 * road_l + road_a, -2 * road_l + road_b),
    (3 * road_l - road_a, -2 * road_l + road_b),
    (3 * road_l + road_a, -2 * road_l + road_b),
    (-1 * road_l - road_a, -road_b),
    (-1 * road_l + road_a, -road_b),
    (3 * road_l - road_a, -road_b),
    (3 * road_l + road_a, -road_b),
    (-1 * road_l + road_b, -road_a),
    (-1 * road_l + road_b, road_a),
    (3 * road_l - road_b, -road_a),
    (3 * road_l - road_b, road_a),
    (-1 * road_l - road_a, road_b),
    (-1 * road_l + road_a, road_b),
    (3 * road_l - road_a, road_b),
    (3 * road_l + road_a, road_b),
    (-3 * road_l - road_a, 2 * road_l - road_b),
    (-3 * road_l + road_a, 2 * road_l - road_b),
    (-1 * road_l - road_a, 2 * road_l - road_b),
    (-1 * road_l + road_a, 2 * road_l - road_b),
    (3 * road_l - road_a, 2 * road_l - road_b),
    (3 * road_l + road_a, 2 * road_l - road_b),
    (-3 * road_l + road_b, 2 * road_l - road_a),
    (-3 * road_l + road_b, 2 * road_l + road_a),
    (-1 * road_l - road_b, 2 * road_l - road_a),
    (-1 * road_l - road_b, 2 * road_l + road_a),
    (-1 * road_l + road_b, 2 * road_l - road_a),
    (-1 * road_l + road_b, 2 * road_l + road_a),
    (3 * road_l - road_b, 2 * road_l - road_a),
    (3 * road_l - road_b, 2 * road_l + road_a),
    (3 * road_l + road_b, 2 * road_l - road_a),
    (3 * road_l + road_b, 2 * road_l + road_a),
    (5 * road_l, 2 * road_l - road_a),
    (5 * road_l, 2 * road_l + road_a),
    (3 * road_l + road_b, -2 * road_l - road_a),
    (3 * road_l + road_b, -2 * road_l + road_a),
    (5 * road_l, -2 * road_l - road_a),
    (5 * road_l, -2 * road_l + road_a),
    (-5 * road_l, 2 * road_l - road_a),
    (-5 * road_l, 2 * road_l + road_a),
    (-3 * road_l - road_b, 2 * road_l - road_a),
    (-3 * road_l - road_b, 2 * road_l + road_a),
]

roads = [
    (nodes[2], nodes[0]),
    (nodes[1], nodes[3]),
    (nodes[6], nodes[4]),
    (nodes[5], nodes[7]),
    (nodes[10], nodes[8]),
    (nodes[9], nodes[11]),
    (nodes[12], nodes[30]),
    (nodes[31], nodes[13]),
    (nodes[14], nodes[18]),
    (nodes[19], nodes[15]),
    (nodes[16], nodes[20]),
    (nodes[21], nodes[17]),
    (nodes[26], nodes[32]),
    (nodes[33], nodes[27]),
    (nodes[28], nodes[34]),
    (nodes[35], nodes[29]),
    (nodes[38], nodes[36]),
    (nodes[37], nodes[39]),
    (nodes[42], nodes[40]),
    (nodes[41], nodes[43]),
    (nodes[46], nodes[44]),
    (nodes[45], nodes[47]),
    (nodes[24], nodes[22]),
    (nodes[23], nodes[25]),
    (nodes[50], nodes[48]),
    (nodes[49], nodes[51]),
    (nodes[54], nodes[52]),
    (nodes[53], nodes[55]),

    (nodes[4], nodes[2]),#28
    (nodes[3], nodes[5]),
    (nodes[8], nodes[6]),
    (nodes[7], nodes[9]),#31
    (nodes[18], nodes[26]),#32
    (nodes[27], nodes[19]),#33
    (nodes[20], nodes[28]),
    (nodes[29], nodes[21]),#35
    (nodes[40], nodes[38]),
    (nodes[39], nodes[41]),#37
    (nodes[44], nodes[42]),
    (nodes[43], nodes[45]),#39
    (nodes[48], nodes[10]),
    (nodes[11], nodes[49]),#41
    (nodes[36], nodes[54]),
    (nodes[55], nodes[37]),
]

curves = [
    *turn_road(nodes[13], nodes[2], TURN_LEFT, curve_r),
    *turn_road(nodes[3], nodes[12], TURN_RIGHT, curve_r),
    *turn_road(nodes[4], nodes[12], TURN_LEFT, curve_r),
    *turn_road(nodes[13], nodes[5], TURN_RIGHT, curve_r),#3
    *turn_road(nodes[15], nodes[6], TURN_LEFT, curve_r),
    *turn_road(nodes[7], nodes[14], TURN_RIGHT, curve_r), #5
    *turn_road(nodes[8], nodes[14], TURN_LEFT, curve_r),
    *turn_road(nodes[15], nodes[9], TURN_RIGHT, curve_r),
    *turn_road(nodes[11], nodes[16], TURN_RIGHT, curve_r), #8
    *turn_road(nodes[17], nodes[10], TURN_LEFT, curve_r),
    *turn_road(nodes[27], nodes[23], TURN_RIGHT, curve_r),
    *turn_road(nodes[22], nodes[26], TURN_LEFT, curve_r),#11
    *turn_road(nodes[22], nodes[19], TURN_RIGHT, curve_r),
    *turn_road(nodes[18], nodes[23], TURN_LEFT, curve_r),#13
    *turn_road(nodes[20], nodes[24], TURN_RIGHT, curve_r),
    *turn_road(nodes[25], nodes[21], TURN_LEFT, curve_r),#15
    *turn_road(nodes[25], nodes[28], TURN_RIGHT, curve_r),
    *turn_road(nodes[29], nodes[24], TURN_LEFT, curve_r),#17
    *turn_road(nodes[36], nodes[31], TURN_RIGHT, curve_r),
    *turn_road(nodes[30], nodes[37], TURN_LEFT, curve_r), #19
    *turn_road(nodes[32], nodes[38], TURN_RIGHT, curve_r),
    *turn_road(nodes[39], nodes[33], TURN_LEFT, curve_r),#21
    *turn_road(nodes[40], nodes[33], TURN_RIGHT, curve_r),
    *turn_road(nodes[32], nodes[41], TURN_LEFT, curve_r),#23
    *turn_road(nodes[34], nodes[42], TURN_RIGHT, curve_r),
    *turn_road(nodes[43], nodes[35], TURN_LEFT, curve_r),#25
    *turn_road(nodes[44], nodes[35], TURN_RIGHT, curve_r),
    *turn_road(nodes[34], nodes[45], TURN_LEFT, curve_r),
    *turn_road(nodes[17], nodes[49], TURN_RIGHT, curve_r),
    *turn_road(nodes[48], nodes[16], TURN_LEFT, curve_r),#29
    *turn_road(nodes[30], nodes[54], TURN_RIGHT, curve_r),
    *turn_road(nodes[55], nodes[31], TURN_LEFT, curve_r),
]


def get_curve(i):
    return range(len(roads) + i * curve_r, len(roads) + (i + 1) * curve_r)


curve_map = {
    (1, 6): get_curve(1),
    (1, 3): [29],
    (2, 0): [28],
    (2, 6): get_curve(2),
    (3, 5): [31],
    (3, 8): get_curve(5),
    (4, 2): [30],
    (4, 8): get_curve(6),
    (5, 10): get_curve(8),
    (5, 25): [41],
    (6, 17): get_curve(19),
    (6, 26): get_curve(30),
    (7, 0): get_curve(0),
    (7, 3): get_curve(3),
    (8, 12): [32],
    (8, 23): get_curve(13),
    (9, 2): get_curve(4),
    (9, 5): get_curve(7),
    (10, 22): get_curve(14),
    (10, 14): [34],
    (11, 4): get_curve(9),
    (11, 25): get_curve(28),
    (12, 16): get_curve(20),
    (12, 19): get_curve(23),
    (13, 9): [33],
    (13, 23): get_curve(10),
    (14, 18): get_curve(24),
    (14, 21): get_curve(27),
    (15, 11): [35],
    (15, 22): get_curve(17),
    (16, 7): get_curve(18),
    (16, 26): [42],
    (17, 13): get_curve(21),
    (17, 19): [37],
    (18, 13): get_curve(22),
    (18, 16): [36],
    (19, 21): [39],
    (19, 15): get_curve(25),
    (20, 15): get_curve(26),
    (20, 18): [38],
    (22, 9): get_curve(12),
    (22, 12): get_curve(11),
    (23, 11): get_curve(15),
    (23, 14): get_curve(16),
    (24, 4): [40],
    (24, 10): get_curve(29),
    (27, 7): get_curve(31),
    (27, 17): [43],
    (1, 0): [],
    (2, 3): [],
    (3, 2): [],
    (4, 5): [],
    (5, 4): [],
    (24, 25): [],
    (6, 7): [],
    (7, 6): [],
    (8, 9): [],
    (9, 8): [],
    (10, 11): [],
    (11, 10): [],
    (22, 23): [],
    (23, 22): [],
    (12, 13): [],
    (13, 12): [],
    (14, 15): [],
    (15, 14): [],
    (27, 26): [],
    (16, 17): [],
    (17, 16): [],
    (18, 19): [],
    (19, 18): [],
    (20, 21): [],
    (0, 1): [],
    (25, 24): [],
    (21, 20): [],
    (26, 27): [],
}


def curve(i, j):
    return curve_map[(i, j)]


nodes2edge = {
    (2, 1): (0, 1),
    (1, 2): (1, 1),
    (3, 2): (2, 1),
    (2, 3): (3, 1),
    (4, 3): (4, 2),
    (3, 4): (5, 2),
    (2, 9): (6, 2),
    (9, 2): (7, 2),
    (3, 6): (8, 1),
    (6, 3): (9, 1),
    (4, 5): (10, 1),
    (5, 4): (11, 1),
    (6, 10): (12, 1),
    (10, 6): (13, 1),
    (5, 11): (14, 1),
    (11, 5): (15, 1),
    (10, 9): (16, 1),
    (9, 10): (17, 1),
    (11, 10): (18, 2),
    (10, 11): (19, 2),
    (12, 11): (20, 1),
    (11, 12): (21, 1),
    (5, 6): (22, 2),
    (6, 5): (23, 2),
    (7, 4): (24, 1),
    (4, 7): (25, 1),
    (9, 8): (26, 1),
    (8, 9): (27, 1)
}

edge2nodes = {}
for nodes, edge in nodes2edge.items():
    edge2nodes[edge[0]] = nodes


road_G = nx.DiGraph()
for i in range(1, 13):
    road_G.add_node(i)
for nodes, edge in nodes2edge.items():
    road_G.add_edge(*nodes, weight=edge[1])
