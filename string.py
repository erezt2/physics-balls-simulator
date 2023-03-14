from vec2 import Vec2
import pygame as pg


class Tail:
    tail_list = []

    def __init__(self, length, width, pos=Vec2(), edge=1):
        self.len = length
        self.w = width
        self.pos = pos
        self.__class__.tail_list.append(self)
        self.edge = edge
        self.par = Vec2()

    def follow(self, head):
        self.pos.y += 10
        pos = head - self.pos
        if abs(pos) != 0:
            pos *= self.len / abs(pos)
            self.pos = head - pos
            self.par = pos / abs(pos)

    def draw(self, window, camera):
        adj = self.par.matrix([[0, -1], [1, 0]]) * self.w / 2
        par = self.par * self.edge
        head = self.pos + self.par * self.len
        pg.draw.polygon(window, (255, 255, 255), [(head + par - adj).fit(camera, False), (head + par + adj).fit(camera, False), (self.pos - par + adj).fit(camera, False), (self.pos - par - adj).fit(camera, False)])