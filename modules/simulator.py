# -*- coding: utf-8 -*-
import numpy as np
import pygame as pg
from pygame import gfxdraw


class Simulator:
    def __init__(self, name, simulation, width=1400, height=900):
        pg.display.set_caption(f'VANET Simulator - {name}')
        self.simulation = simulation
        self.screen = None

        self.width, self.height = width, height
        self.background_color = (47, 129, 48)
        self.text_font = None

        self.fps = 60
        self.zoom = 5
        self.offset = (0, 0)
        self.mouse_last = (0, 0)
        self.mouse_down = False

    def loop(self, simulation_runner=None):
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.flip()
        clock = pg.time.Clock()
        pg.font.init()
        self.text_font = pg.font.SysFont('Lucida Console', 16)

        done = False
        while not done:
            if simulation_runner:
                simulation_runner(self.simulation)

            self.draw()
            pg.display.update()
            clock.tick(self.fps)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

                elif event.type == pg.MOUSEBUTTONDOWN:
                    zoom = (self.zoom ** 2 + self.zoom / 4 + 1) / (self.zoom ** 2 + 1)
                    if event.button == 1:
                        x0, y0 = self.offset
                        x1, y1 = pg.mouse.get_pos()
                        self.mouse_last = x1 - x0 * self.zoom, y1 - y0 * self.zoom
                        self.mouse_down = True
                    elif event.button == 4:
                        self.zoom *= zoom
                    elif event.button == 5:
                        self.zoom /= zoom

                elif event.type == pg.MOUSEMOTION:
                    if self.mouse_down:
                        x0, y0 = self.mouse_last
                        x1, y1 = pg.mouse.get_pos()
                        self.offset = (x1 - x0) / self.zoom, (y1 - y0) / self.zoom
                elif event.type == pg.MOUSEBUTTONUP:
                    self.mouse_down = False

    def run(self, steps=1):
        def runner(simulation):
            simulation.run(steps)
        self.loop(runner)

    def convert_sim2screen(self, x, y=None):
        if isinstance(x, list):
            return [self.convert_sim2screen(e[0], e[1]) for e in x]
        elif isinstance(x, tuple):
            return self.convert_sim2screen(*x)
        x_screen = int(self.width / 2 + (x + self.offset[0]) * self.zoom)
        y_screen = int(self.height / 2 + (y + self.offset[1]) * self.zoom)
        return x_screen, y_screen

    def convert_screen2sim(self, x, y=None):
        if isinstance(x, list):
            return [self.convert_screen2sim(e[0], e[1]) for e in x]
        elif isinstance(x, tuple):
            return self.convert_screen2sim(*x)
        x_sim = int(-self.offset[0] + (x - self.width / 2) / self.zoom)
        y_sim = int(-self.offset[1] + (y - self.height / 2) / self.zoom)
        return x_sim, y_sim

    def draw_box(self, pt, size, sin=None, cos=None, centered=True, color=None):
        color = color or (0, 0, 255)
        x, y = pt
        l, h = size
        vertex = lambda e1, e2: (x + (e1 * l * cos + e2 * h * sin) / 2,
                                 y + (e1 * l * sin - e2 * h * cos) / 2)
        if centered:
            dirs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
            vertices = self.convert_sim2screen([vertex(*e) for e in dirs])
        else:
            dirs = [(0, -1), (0, 1), (2, 1), (2, -1)]
            vertices = self.convert_sim2screen([vertex(*e) for e in dirs])
        gfxdraw.filled_polygon(self.screen, vertices, color)

    def draw_arrow(self, pt, size, sin=None, cos=None, color=None):
        color = color or (150, 150, 190)
        self.draw_box(pt, size, sin=(cos + sin) / np.sqrt(2),
                      cos=(cos - sin) / np.sqrt(2), color=color, centered=False)
        self.draw_box(pt, size, sin=(sin - cos) / np.sqrt(2),
                      cos=(sin + cos) / np.sqrt(2), color=color, centered=False)

    def draw_roads(self):
        for road in self.simulation.roads:
            self.draw_box(road.start, (road.length, 3.7), sin=road.sin, cos=road.cos,
                          color=(180, 180, 220), centered=False)

            if road.length > 5:
                for i in np.arange(-0.5 * road.length, 0.5 * road.length, 10):
                    pt_x = road.start[0] + (road.length / 2 + i + 3) * road.cos
                    pt_y = road.start[1] + (road.length / 2 + i + 3) * road.sin
                    pt = (pt_x, pt_y)
                    self.draw_arrow(pt, (-1.25, 0.2), sin=road.sin, cos=road.cos)

    def draw_vehicles(self):
        for road in self.simulation.roads:
            for vehicle in road.vehicles:
                l, h = vehicle.length, 2
                sin, cos = road.sin, road.cos
                x = road.start[0] + cos * vehicle.x
                y = road.start[1] + sin * vehicle.x
                self.draw_box((x, y), (l, h), sin=sin, cos=cos)

    def draw_signs(self):
        green, red = (0, 255, 0), (255, 0, 0)
        for sign in self.simulation.traffic_signs:
            for i in range(len(sign.roads)):
                color = green if sign.current_cycle[i] else red
                for road in sign.roads[i]:
                    pt = (road.end[0], road.end[1])
                    self.draw_box(pt, (1, 3), sin=road.sin, cos=road.cos, color=color)

    def draw_rsus(self):
        white = (255, 255, 255)
        red = (255, 0, 0)
        for road in self.simulation.roads:
            if road.rsu:
                l = 4
                sin, cos = road.sin, road.cos
                x = road.start[0] + cos * road.rsu.x
                y = road.start[1] + sin * road.rsu.x
                color = red if road.rsu.active else white
                self.draw_box((x, y), (l, l), sin=sin, cos=cos, color=color)
                sim_coord = self.convert_sim2screen(x - l // 2, y - l // 2)
                self.screen.blit(self.text_font.render('R', False, (0, 0, 0)), sim_coord)

    def draw_status(self):
        text_fps = self.text_font.render(f'Time: {self.simulation.t:.3f}', False, (0, 0, 0))
        avg_time = 0. if self.simulation.arrived == 0 else self.simulation.elapsed / self.simulation.arrived
        text_mean = self.text_font.render(f'Avg. elapsed time: {avg_time:.3f}', False, (0, 0, 0))
        # max_vehicles = self.text_font.render(f'Max Vehicles: {self.simulation.max_traffic}', False, (0, 0, 0))

        self.screen.blit(text_fps, (0, 0))
        self.screen.blit(text_mean, (0, 20))
        # self.screen.blit(max_vehicles, (0, 40))

    def draw(self):
        self.screen.fill(self.background_color)
        self.draw_roads()
        self.draw_vehicles()
        self.draw_signs()
        self.draw_rsus()
        self.draw_status()
