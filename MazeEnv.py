import os
import numpy as np
from graphs import Point, Ray, Segment

ROBOT_SIZE = 5
END_SIZE = 5
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
STEP_SIZE = 10
SENSOR_IDX = [0, 1, 2, 4, 6, 7]
TARGET_SENSOR_DIRECTION = [0, 2, 4, 6]

TWO_2 = np.sqrt(2) / 2


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


class MazeEnv(object):
    def __init__(self, maze_index, time_limit=1000):
        self.maze_index = maze_index
        self.time_limit = time_limit
        file = os.path.join("Mazes", f"maze_{maze_index}")

        self.start, self.end, self.maze_lines = parseFile(file)
        self.start = Point(self.start[0], self.start[1])
        self.end = Point(self.end[0], self.end[1])
        self.map_wall = []

        for line in self.maze_lines:
            self.map_wall.append(Segment(line[0], line[1], line[2], line[3]))

        self.robot_pos = Point(self.start.x, self.start.y)
        # self.robot_face = random_face()
        self.robot_face = DIRECTIONS[0]

        self.eight_directions = self.get_eight_directions()

        self.time = 0

    def robot_turn_left(self):
        if self.robot_face == (1, 0):
            self.robot_face = 0, 1
        elif self.robot_face == (0, 1):
            self.robot_face = -1, 0
        elif self.robot_face == (-1, 0):
            self.robot_face = 0, -1
        elif self.robot_face == (0, -1):
            self.robot_face = 1, 0
        else:
            raise ValueError("Invalid direction")
        self.eight_directions = self.get_eight_directions()

    def robot_turn_right(self):
        if self.robot_face == (1, 0):
            self.robot_face = 0, -1
        elif self.robot_face == (0, 1):
            self.robot_face = 1, 0
        elif self.robot_face == (-1, 0):
            self.robot_face = 0, 1
        elif self.robot_face == (0, -1):
            self.robot_face = -1, 0
        else:
            raise ValueError("Invalid direction")
        self.eight_directions = self.get_eight_directions()

    def collision(self):
        for wall in self.map_wall:
            if wall.distance(self.robot_pos) < ROBOT_SIZE:
                return True
        return False

    def robot_walk_forward(self):
        self.robot_pos.x += self.robot_face[0] * STEP_SIZE
        self.robot_pos.y += self.robot_face[1] * STEP_SIZE
        if self.collision():
            self.robot_pos.x -= self.robot_face[0] * STEP_SIZE
            self.robot_pos.y -= self.robot_face[1] * STEP_SIZE
            return False
        return True

    def robot_walk_backward(self):
        self.robot_pos.x -= self.robot_face[0] * STEP_SIZE
        self.robot_pos.y -= self.robot_face[1] * STEP_SIZE
        if self.collision():
            self.robot_pos.x += self.robot_face[0] * STEP_SIZE
            self.robot_pos.y += self.robot_face[1] * STEP_SIZE
            return False
        return True

    def get_eight_directions(self):
        rotate_matrix = np.array([[TWO_2, -TWO_2], [TWO_2, TWO_2]])
        current_direction = np.array(self.robot_face)
        eight_directions = []
        for i in range(8):
            eight_directions.append(current_direction)
            current_direction = rotate_matrix.dot(current_direction)
        return eight_directions

    '''
      0
    1   3
      2  
    '''
    def end_point_direction(self):
        d = (self.end.x - self.robot_pos.x, self.end.y - self.robot_pos.y)
        target_sensor_direction = [self.eight_directions[i] for i in TARGET_SENSOR_DIRECTION]
        target_sensor_angle = []
        for direction in target_sensor_direction:
            angle_val = np.arccos(np.dot(d, direction) / (np.linalg.norm(d) * np.linalg.norm(direction)))
            target_sensor_angle.append(angle_val)
        print(target_sensor_angle)
        return np.argmin(target_sensor_angle)

    '''
            0       .............(face)   
          1   7
        2       6
          3   5 
            4      
    '''
    def observation(self):
        sensor_rays = [self.robot_pos.create_ray(self.eight_directions[i]) for i in SENSOR_IDX]
        sensor_vals = []
        for ray in sensor_rays:
            walls_distance = [ray.distance(wall) for wall in self.map_wall]
            sensor_vals.append(min(walls_distance))
        return sensor_vals, self.end_point_direction()

    def get_angle(self):
        d = (self.end.x - self.robot_pos.x, self.end.y - self.robot_pos.y)
        angle = np.arctan2(d[1], d[0])
        return angle

if __name__ == '__main__':
    env = MazeEnv(55)

    print(env.observation())
