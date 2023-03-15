from vec2 import Vec2
from helper import WINDOW_HEIGHT, WINDOW_WIDTH
import pygame as pg


class Node:
    def __init__(self, body, pos, radius=8, mass=1.0, charge=1, locked=False, color=(80, 80, 255)):
        self.pos = Vec2(pos)
        self.vel = Vec2()
        self.forces = Vec2()
        self.mass = mass
        self.charge = charge
        self.radius = radius
        self.branches = []
        self.locked = locked
        self.color = color
        self.body = body

    def apply_force(self, mode):
        return Vec2(0, -800) * self.mass
        _sum = Vec2()
        for node in self.body.nodes:
            if node == self:
                continue
            _sum -= (self.pos - node.pos) / abs(self.pos - node.pos) ** 3 * (self.charge * node.charge * 1000000)

        if "yeet" in mode:
            x = self.pos.x - WINDOW_WIDTH//2
            _sum += Vec2(-x, 0)
        if "gravity" in mode:
            _sum += Vec2(0, -800) * self.mass
        elif "inward_gravity" in mode:
            _sum += Vec2(WINDOW_WIDTH // 2 - self.pos.x, WINDOW_HEIGHT // 2 - self.pos.y) * self.mass
        return _sum

    def draw(self, window, camera):
        try:
            pg.draw.circle(window, self.color, self.pos.fit(camera), self.radius)
        except:
            print(window, self.color, self.pos.fit(camera), self.radius)
        # pg.draw.line(Win.win, (255, 255, 255), self.pos.fit(), (self.pos + self.vel / 20).fit(), 2)

    def calculate_frame(self, dt):
        if self.locked:
            self.vel = 0
        else:
            self.vel += self.forces / self.mass / dt
            temp = Vec2(self.pos)
            self.pos += self.vel / dt

            for hitbox in self.body.hitboxes:
                _check = self.pos.lines_collide(temp, hitbox.pos1, hitbox.pos2)

                if not _check and not hitbox.get_box(self.radius + hitbox.thickness + 3).collidepoint(self.pos.x, self.pos.y):
                    continue

                vec = hitbox.vector_orthogonal(self.pos)
                orthogonal = abs(vec)
                horizontal = hitbox.distance_horizontal(self.pos)

                if not _check and orthogonal >= -(hitbox.thickness // -2) + self.radius and horizontal >= self.radius:
                    continue

                elif not _check and (max(orthogonal + (hitbox.thickness // -2), 0.0)) ** 2 + horizontal ** 2 < self.radius ** 2:
                    _check = True

                    # temp = hitbox.normal * (hitbox.distance_horizontal(self.pos) - 0.707)
                    # self.pos -= temp
                if _check:
                    self.pos += hitbox.normal * (self.radius - (hitbox.thickness // -2)) - vec
                    self.vel -= hitbox.normal * (2 * (self.vel * hitbox.normal))
                    self.vel *= hitbox.bounce
                    hitbox.hit_func(self)
                    for node in self.body.nodes:
                        if node == self:
                            continue
                        if (node.pos - self.pos).length2() < (self.radius + node.radius) ** 2:
                            node.pos += hitbox.normal * (self.radius - (hitbox.thickness // -2)) - vec

        for node in self.body.nodes:
            if node == self:
                continue
            if (node.pos - self.pos).length2() <= (self.radius + node.radius) ** 2:
                self_vel = self.vel
                temp = self.pos - node.pos
                self.vel -= temp * (2 * node.mass / (node.mass + self.mass) * ((self.vel - node.vel) * temp) / temp.length2())
                node.vel -= temp * (2 * self.mass / (self.mass + node.mass) * ((node.vel - self_vel) * temp) / temp.length2())
                # radius = (self.radius + node.radius) ** 2
                # dx = self.pos - node.pos
                # dv = self.vel - node.vel
                # temp = 2 * dx.x * dx.y + dv.x * dv.y - (dx.x * dv.y) ** 2 - (dx.y * dv.x) ** 2
                # x = ((radius * dv.length2() + temp) ** (1/2) - dx * dv) / (dv.length2())
                # self.pos += self.vel * x
                # node.pos += node.vel * x
                offset = (self.pos - node.pos) / abs(self.pos - node.pos) * (self.radius + node.radius - abs(self.pos - node.pos))
                self.pos += offset / 2
                node.pos -= offset / 2
