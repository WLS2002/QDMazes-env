import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def create_ray(self, direction):
        return Ray(self.x, self.y, direction[0], direction[1])

    def distance(self, p):
        return np.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2)


class Segment:

    # Ax + By + C = 0
    def __init__(self, x1, y1, x2, y2):
        assert x1 != x2 or y1 != y2, "Segment cannot be a point"

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.end1 = Point(self.x1, self.y1)
        self.end2 = Point(self.x2, self.y2)

    # get the distance from a point to the segment
    def distance(self, p: Point):
        vertical_ray = p.create_ray((self.A, self.B))
        inner_point = get_inner_point(self.A, self.B, self.C, vertical_ray.A, vertical_ray.B, vertical_ray.C)
        if self.is_point_on(inner_point):
            return p.distance(inner_point)
        else:
            return min(p.distance(self.end1), p.distance(self.end2))

    def is_point_on(self, p: Point):
        if self.A * p.x + self.B * p.y + self.C > 1e-6:
            return False
        if (p.x - self.x1) * (p.x - self.x2) > 1e-6:
            return False
        if (p.y - self.y1) * (p.y - self.y2) > 1e-6:
            return False
        return True


class Ray:
    # Ax + By + C = 0
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        self.A = self.dy
        self.B = -self.dx
        self.C = self.dx * self.y - self.dy * self.x

    def distance(self, s: Segment):
        inner_point = get_inner_point(self.A, self.B, self.C, s.A, s.B, s.C)
        if inner_point is None:
            return np.inf
        if self.is_point_on(inner_point) and s.is_point_on(inner_point):
            return inner_point.distance(Point(self.x, self.y))
        else:
            return np.inf

    def is_point_on(self, p: Point):
        if self.A * p.x + self.B * p.y + self.C > 1e-6:
            return False
        if (p.x - self.x) * self.dx < -1e-6:
            return False
        if (p.y - self.y) * self.dy < -1e-6:
            return False
        return True


def get_inner_point(A1, B1, C1, A2, B2, C2):
    det = A1 * B2 - A2 * B1
    if det == 0:
        return None
    else:
        x = (B2 * C1 - B1 * C2) / det
        y = (A1 * C2 - A2 * C1) / det
        return Point(-x, -y)


if __name__ == '__main__':
    # zero = Point(0, 0)
    # one = Point(1, 1)
    # two = Point(2, 2)
    #
    # r1 = two.create_ray((-1.5, -1))
    # r2 = two.create_ray((1, 1))
    #
    # s1 = Segment(-1, 1, 1, 1)
    # print(s1.distance(zero))
    # print(s1.distance(one))
    # print(s1.distance(two))
    # print(r1.distance(s1))
    # print(r2.distance(s1))
    # TWO_2 = np.sqrt(2) / 2
    # rotate_matrix = np.array([[TWO_2, -TWO_2], [TWO_2, TWO_2]])
    # current_direction = np.array((0, 1))
    # eight_directions = []
    # for i in range(8):
    #     eight_directions.append(current_direction)
    #     current_direction = rotate_matrix.dot(current_direction)
    # print(eight_directions)
    r = Ray(10, 10, 0, 1.0000000000000002)
    s = Segment(0, 200, 200, 200)
    print(r.distance(s))
