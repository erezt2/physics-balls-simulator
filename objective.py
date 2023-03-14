from vec2 import Vec2
import pygame as pg


class Area:
    def __init__(self, pos, size, color=(255, 255, 255), func="none"):
        self.info = {}
        self.pos = Vec2(pos)
        self.size = Vec2(size)
        self.color = color
        self.func = func
        print(color)

    def draw(self, window, camera):
        pg.draw.rect(window, self.color, (*self.pos.fit(camera), *self.size.fit(camera, False)))

    def calculate_frame(self, node, func_list):
        dx1 = node.pos.x - self.pos.x
        dx2 = node.pos.x - self.pos.x - self.size.x
        if dx1 * dx2 <= 0:
            dx = 0
        else:
            dx = min(dx1, dx2)

        dy1 = node.pos.y - self.pos.y
        dy2 = node.pos.y - self.pos.y - self.size.y
        if dy1 * dy2 <= 0:
            dy = 0
        else:
            dy = min(dy1, dy2)

        if dx < node.radius and dy < node.radius:
            if dx ** 2 + dy ** 2 < node.radius ** 2:
                if isinstance(self.func, str):
                    func_list[self.func](self, node)
                else:
                    self.func(self, node)
