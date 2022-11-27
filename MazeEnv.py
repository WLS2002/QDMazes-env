import os
import numpy as np

ROBOT_SIZE = 5
END_SIZE = 5
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parseFile(folder):
    maze_lines = []
    start = []
    end = []

    with open(folder, "r") as myfile:

        lines = myfile.readlines()

        start = [int(int(lines[1].split(" ")[0])),
                 int((int(lines[1].split(" ")[1])))]

        end = [int(int(lines[3].split(" ")[0])),
               int((int(lines[3].split(" ")[1])))]

        lines = lines[4:]

        for line in lines:
            if line in ["\n"]:
                continue

            else:
                data = line.split(" ")

                maze_lines += [[int(int(data[0])), int((int(data[1]))),
                                int(int(data[2])), int((int(data[3])))]]

    return start, end, maze_lines


# gives a random direction
def random_face():
    return DIRECTIONS[np.random.randint(len(DIRECTIONS))]


# receives a direction and returns the left-side direction
def turn_left(direction):
    if direction == (1, 0):
        return 0, 1
    elif direction == (0, 1):
        return -1, 0
    elif direction == (-1, 0):
        return 0, -1
    elif direction == (0, -1):
        return 1, 0
    else:
        raise ValueError("Invalid direction")


# receives a direction and returns the left-side direction
def turn_right(direction):
    if direction == (1, 0):
        return 0, -1
    elif direction == (0, 1):
        return 1, 0
    elif direction == (-1, 0):
        return 0, 1
    elif direction == (0, -1):
        return -1, 0
    else:
        raise ValueError("Invalid direction")


# calculates the distance between a point and a segment
def distance_point_segment(p_x, p_y, x_0, y_0, x_1, y_1):
    if x_0 == x_1:
        line_distance = abs(p_x - x_0)
    elif y_0 == y_1:
        line_distance = abs(p_y - y_0)
    else:
        m = (y_1 - y_0) / (x_1 - x_0)
        b = y_0 - m * x_0
        line_distance = abs(m * p_x - p_y + b) / np.sqrt(m ** 2 + 1)

    left_end_distance = np.sqrt((p_x - x_0) ** 2 + (p_y - y_0) ** 2)
    right_end_distance = np.sqrt((p_x - x_1) ** 2 + (p_y - y_1) ** 2)
    return min(line_distance, left_end_distance, right_end_distance)


# calculates the length of a ray from point to a line
def ray_length(p_x, p_y, r_d_x, r_d_1, x_0, y_0, x_1, y_1):
    if x_0 == x_1:
        if r_d_x == 0:
            return np.inf
        else:
            return (x_0 - p_x) / r_d_x
    elif y_0 == y_1:
        if r_d_1 == 0:
            return np.inf
        else:
            return (y_0 - p_y) / r_d_1
    else:
        m = (y_1 - y_0) / (x_1 - x_0)
        b = y_0 - m * x_0
        if m * r_d_x - r_d_1 == 0:
            return np.inf
        else:
            return (m * p_x - p_y + b) / (m * r_d_x - r_d_1)


class MazeEnv(object):
    def __init__(self, maze_index, time_limit=1000):
        self.maze_index = maze_index
        self.time_limit = time_limit
        file = os.path.join("Mazes", f"maze_{maze_index}")

        self.start, self.end, self.maze_lines = parseFile(file)

        self.robot_pos = self.start
        self.robot_face = random_face()
        self.time = 0


if __name__ == '__main__':
    env = MazeEnv(55)
