import pygame as pg
from helper import min_max


class Branch:
    def __init__(self, node1, node2, length, strength=8, damping=0, color=(80, 255, 80)):
        self.node1 = node1
        self.node2 = node2
        self.length = length
        self.strength = strength
        self.color = color
        self.damping = damping
        node1.branches.append(self)
        node2.branches.append(self)

    def apply_node_forces(self):
        parallel = self.node2.pos - self.node1.pos
        force = ((abs(parallel) - self.length) * self.strength)
        damp = (self.node2.vel - self.node1.vel) * parallel / abs(parallel) * self.damping
        parallel /= abs(parallel)

        self.node1.forces += parallel * (force + damp)
        self.node2.forces -= parallel * (force + damp)

    def __len__(self):
        return abs(self.node2 - self.node1)

    def draw(self, window, camera):
        const = (1 - self.length / abs(self.node2.pos - self.node1.pos) / 2)
        pg.draw.line(window, [min_max(0, i * const, 255) for i in self.color], self.node1.pos.fit(camera), self.node2.pos.fit(camera), 1)
