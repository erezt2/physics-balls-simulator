import functools

from spring import Branch
from vec2 import Vec2
from window import Win
import pygame as pg
from random import randint


class Polygon:
    def __init__(self, body, polygon):
        if len(polygon) < 3:
            return

        polygon = [body.nodes[node] for node in polygon]

        n = len(polygon)
        for i in range(len(polygon)):
            body.branches.append(Branch(polygon[i], polygon[(i+1)%n], 15, 120, 3))

        self.polygon = polygon

    @staticmethod
    def calc_triangle_area(node1, node2, node3):
        a = (node1.pos-node2.pos).length()
        b = (node2.pos-node3.pos).length()
        c = (node3.pos-node1.pos).length()
        s = (a+b+c)/2
        return (s*(s-a)*(s-b)*(s-c))**(1/2)

    def get_polygon_area(self):
        area = 0
        for i in range(1, len(self.polygon)-1):
            area += self.calc_triangle_area(self.polygon[0], self.polygon[i], self.polygon[i+1])
        return area

    @staticmethod
    def handle_area(area):
        if area < 10:
            return 10
        return 1 / area**(1/2)

    @staticmethod
    def handle_length(node, center):
        return 1 / (node.pos - center).length()

    def apply_forces(self):
        MULT = 200 * 100**2  # * 100 ** 2
        area = self.get_polygon_area()
        center = sum(map(lambda x: x.pos*x.mass, self.polygon), Vec2()) / sum(map(lambda x: x.mass, self.polygon))

        lengths = list(map(lambda x: self.handle_length(x, center), self.polygon))

        pos_lengths = list(zip(self.polygon, lengths))

        center2 = sum(map(lambda x: x[0].pos * x[1], pos_lengths), Vec2()) / sum(lengths)

        pg.draw.circle(Win.win, (255, 255, 0), center.fit(Win.camera), 3, 1)
        pg.draw.circle(Win.win, (0, 255, 255), center2.fit(Win.camera), 3, 1)
        _sum = Vec2()
        for node, length in pos_lengths:
            node.forces += (node.pos - center2) * MULT * length * self.handle_area(area)
        return

    def apply_forces1(self):
        area = self.get_polygon_area()
        MULT = 200 * 400 ** 2
        n = len(self.polygon)
        _sum = Vec2()
        for i in range(len(self.polygon)):
            left = self.polygon[(i - 1) % n]
            right = self.polygon[(i + 1) % n]
            normal = (left.pos - right.pos)
            normal /= normal.length()
            ortho = normal.reverse()
            ortho.y *= -1
            node = self.polygon[i]
            temp = ortho / area * MULT
            node.forces += temp
            _sum += temp
        for node in self.polygon:
            node.forces -= _sum / n