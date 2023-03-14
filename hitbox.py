from vec2 import Vec2
import pygame as pg


class Hitbox:
    def __init__(self, pos1, pos2, flipped=False, thickness=3, color=(255, 80, 80), bounce=0.97, hit_func=lambda self: None):
        pos1 = Vec2(pos1)
        pos2 = Vec2(pos2)
        self.pos1 = pos1
        self.pos2 = pos2
        self.parallel = (pos1 - pos2) / abs(pos1 - pos2)
        self.normal = self.parallel.matrix([[0, -1], [1, 0]]) * (-1 if flipped else 1)
        self.bounce = bounce
        self.thickness = thickness
        self.color = color
        self.hit_func = hit_func

    def get_box(self, _offset=1):
        a = pg.Rect((min(self.pos1.x, self.pos2.x) - _offset, min(self.pos1.y, self.pos2.y) - _offset,
                            abs(self.pos1.x - self.pos2.x) + 2 * _offset, abs(self.pos1.y - self.pos2.y) + 2 * _offset))
        # pg.draw.rect(Win.win, (255, 255, 255), a, 1)
        return a

    def draw(self, window, camera_pos):
        pg.draw.line(window, self.color, self.pos1.fit(camera_pos), self.pos2.fit(camera_pos), self.thickness)

    def draw_normal(self, window, camera_pos):
        pg.draw.line(window, self.color, ((self.pos1 + self.pos2) / 2).fit(camera_pos), ((self.pos1 + self.pos2) / 2 + self.normal * 6).fit(), 2)

    def distance_orthogonal(self, point):
        pos1cords = (point - self.pos1)
        return abs(pos1cords - self.parallel * (pos1cords * self.parallel))

    def vector_orthogonal(self, point):
        pos1cords = (point - self.pos1)
        return pos1cords - self.parallel * (pos1cords * self.parallel)

    def in_between(self, point1, point2):
        pos1cords = (point1 - self.pos1)
        pos2cords = (point2 - self.pos1)
        dist1 = pos1cords - self.parallel * (pos1cords * self.parallel)
        dist2 = pos2cords - self.parallel * (pos2cords * self.parallel)

        if dist1 * dist2 <= 0:
            return True
        return False

    def distance_horizontal(self, point):
        dist1 = (point - self.pos1) - self.normal * ((point - self.pos1) * self.normal)
        dist2 = (point - self.pos2) - self.normal * ((point - self.pos2) * self.normal)

        if dist1 * dist2 <= 0:
            return 0.0
        return min(abs(dist1), abs(dist2))