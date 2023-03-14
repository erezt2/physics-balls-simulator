from helper import *


class Vec2:
    def __init__(self, pos=None, pos1=None):
        if pos is None:
            self.x = 0.0
            self.y = 0.0
        elif pos1 is not None:
            self.x = float(pos)
            self.y = float(pos1)
        elif isinstance(pos, Vec2):
            self.x = pos.x
            self.y = pos.y
        else:
            self.x = float(pos[0])
            self.y = float(pos[1])

        self.pos = self

    def __getitem__(self, item):
        if item == 0:
            return self.x
        else:
            return self.y

    def __add__(self, other):
        # if isinstance(other, tuple):
        #     if len(other) != 2:
        #         raise Exception
        #     return Vec2(self.x + other[0], self.y + other[1])
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        # if isinstance(other, tuple):
        #     if len(other) != 2:
        #         raise Exception
        #     return Vec2(self.x - other[0], self.y - other[1])
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if other.__class__ in (float, int):
            return Vec2(self.x * other, self.y * other)
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        raise TypeError

    def __truediv__(self, other):
        if other.__class__ in (int, float):
            return Vec2(self.x / other, self.y / other)

    def __abs__(self):
        return (self * self) ** 0.5

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def length2(self):
        return self * self

    def length(self):
        return (self*self)**(1/2)

    def normal(self):
        return self / self.length()

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def matrix(self, mat2):
        return Vec2(mat2[0][0] * self.x + mat2[0][1] * self.y, mat2[1][0] * self.x + mat2[1][1] * self.y)

    def fit(self, camera_pos, camera=True):
        if camera:
            temp = self + camera_pos
            return round(temp.x), round(temp.y)
        else:
            return round(self.x), round(self.y)

    def line(self, other):
        slope = (self.y - other.y) / (self.x - other.x)
        x0 = self.y - slope * self.x
        return slope, x0

    def reverse(self):
        return Vec2(self.y, self.x)

    def lines_collide(self, point1, point2, point3):
        if self.x == point1.x and point2.x == point3.x:
            if self.x == point2.x and both_ranges(point2.y, self.y, point3.y):
                return True
        elif self.x == point1.x:
            if both_ranges(point2.x, self.x, point3.x):
                line = point2.line(point3)
                y = line[0] * self.x + line[1]
                if both_ranges(self.y, y, point1.y):
                    return True
        elif point2.x == point3.x:
            if both_ranges(self.x, point2.x, point1.x):
                line = self.line(point1)
                y = line[0] * point2.x + line[1]
                if both_ranges(point2.y, y, point3.y):
                    return True
        else:
            m1, c1 = self.line(point1)
            m2, c2 = point2.line(point3)
            if m1 == m2:
                if c1 == c2 and (both_ranges(point2.x, self.x, point3.x)
                        or both_ranges(point2.x, point1.x, point3.x)):
                    return True
            else:
                x = (c2 - c1) / (m1 - m2)
                if both_ranges(self.x, x, point1.x) and both_ranges(point2.x, x, point3.x):
                    return True
        return False

    def mirror(self, x=False, y=True):
        if y:
            ry = WINDOW_HEIGHT - self.y
        else:
            ry = self.y
        if x:
            rx = WINDOW_WIDTH - self.x
        else:
            rx = self.x
        return Vec2(rx, ry)