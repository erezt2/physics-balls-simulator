from vec2 import Vec2
from window import Win
from node import Node
from hitbox import Hitbox
from objective import Area


def accelerate(self, node):
    if node.vel == Vec2():
        return
    node.vel += node.vel.normal() * 4


class Body:
    # ins = None
    components = {
        "small mass ball": ["Node", 4, 0.5, 0],
        "big mass ball": ["Node", 12, 2, 0],
        "small charged ball": ["Node", 4, 0.25, 1],
        "small negatively charged ball": ["Node", 4, 1, -1],
        "light spring": ["Branch"],
        "accelerator": ["Area", (80, 80), (80, 255, 10), accelerate]
    }

    def __init__(self, size=None, toolbox=(), color=(0, 0, 0)):
        if size is None:
            size = Vec2(Win.width, Win.height)
        else:
            size = Vec2(size)

        self.width = size[0]
        self.height = size[1]
        self.main_node = Node(self, Vec2(size.x//2, size.y//2), color=(80, 255, 80))
        self.nodes = [self.main_node]
        self.branches = []
        self.hitboxes = [Hitbox((-10, 0), (size.x+10, 0), True), Hitbox((0, -10), (0, size.y+10)),
                         Hitbox((size.x, -10), (size.x, size.y+10), True), Hitbox((-10, size.y), (size.x+10, size.y))]
        self.areas = [Area((0, 0), (25, 25), func="quit")]
        self.polygons = []
        self.bg_color = color
        # node - radius mass color
        # spring - rest-length strength damping color
        self.toolbox = ["small charged ball", "353ff 4rejr 34fe", "fd", "accelerator", "small mass ball", "big mass ball"]

    def choose_nearest_node(self, pos, nodes=None):
        if nodes is None:
            nodes = self.nodes
        if not nodes:
            return
        pos = Vec2(pos)
        n = None
        _min = float("inf")

        for node in range(len(nodes)):
            l = (pos - nodes[node].pos).length2()
            if l < _min:
                n = node
                _min = l
        return n

    def remove_node(self, index):
        if index is None:
            return
        self.branches = list(filter(lambda x: x not in self.nodes[index].branches, self.branches))
        self.nodes.pop(index)

    def remove_branch(self, index):
        if index is None:
            return
        node2 = self.branches[index].node2
        self.remove_node(self.nodes.index(self.branches[index].node1))
        self.remove_node(self.nodes.index(node2))

    def remove_hitbox(self, index):
        if index is None:
            return
        self.hitboxes.pop(index)

    def choose_nearest_hitbox(self, pos,):
        if len(self.hitboxes) <= 4:
            return None
        pos = Vec2(pos)

        n = None
        _min = float("inf")
        for hitbox in range(len(self.hitboxes[4:])):
            l = self.hitboxes[hitbox+4].distance_orthogonal(pos) ** 2 + self.hitboxes[hitbox+4].distance_horizontal(pos) ** 2
            if l < _min:
                n = hitbox
                _min = l
        return n + 4