import gym
from gym import Env
from gym.error import DependencyNotInstalled

from mazeGame import MazeGame
from gym import spaces
import numpy as np

metadata = {
    "render_modes": ["human", "rgb_array"],
}

class MazeEnv(Env):

    # observation: [distance of sensor] * 6 + [end direction] * 1
    # action: {0: turn left, 1: turn right, 2: walk forward, 3: walk backward}
    def __init__(self, maze_idx, render_mode=None):
        self.metadata = metadata

        self.mazeGame = MazeGame(maze_idx)
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=200, shape=(7,))

        self.end_distance = self.mazeGame.end.distance(self.mazeGame.robot_pos)
        self.TIME_PENALTY = -1

        self.render_mode = render_mode
        self.screen = None
        self.ZOOM = 4
        self.SCREEN_SIZE = 200 * self.ZOOM



    def step(self, action):
        self.mazeGame.action(action)
        terminated, truncated = self.mazeGame.isEnd()
        observation = self.mazeGame.observation()
        observation = self._go2eo(observation)
        reward = self._reward()

        info = {'robot_pos': self.mazeGame.robot_pos, 'robot_face': self.mazeGame.robot_face,
                'start': self.mazeGame.start, 'end': self.mazeGame.end, 'time': self.mazeGame.time,
                'time_limit': self.mazeGame.time_limit, 'TIME_PENALTY': self.TIME_PENALTY}
        self.end_distance = self.mazeGame.end.distance(self.mazeGame.robot_pos)
        return observation, reward, terminated, truncated, info

    def reset(self, *args, **kwargs):
        self.end_distance = self.mazeGame.end.distance(self.mazeGame.start)
        self.mazeGame.reset()
        observation = self.mazeGame.observation()
        observation = self._go2eo(observation)
        info = {'robot_pos': self.mazeGame.robot_pos, 'robot_face': self.mazeGame.robot_face,
                'start': self.mazeGame.start, 'end': self.mazeGame.end, 'time': self.mazeGame.time,
                'time_limit': self.mazeGame.time_limit, 'TIME_PENALTY': self.TIME_PENALTY}
        return observation, info

    def render(self, mode='human'):
        if self.render_mode is None:
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        try:
            import pygame
            from pygame import gfxdraw
        except ImportError:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gym[classic_control]`"
            )
        if self.screen is None:
            pygame.init()
            if self.render_mode == "human":
                pygame.display.init()
                self.screen = pygame.display.set_mode(
                    (self.SCREEN_SIZE, self.SCREEN_SIZE)
                )
            else:  # mode == "rgb_array"
                self.screen = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE))


        self.screen.fill((255, 255, 255))
        for line in self.mazeGame.maze_lines:
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                self.mc2pc(*line[:2]),
                self.mc2pc(*line[2:]),
                1
            )
        pygame.draw.circle(
            self.screen,
            (0, 0, 255),
            self.mc2pc(self.mazeGame.start.x, self.mazeGame.start.y),
            5 * self.ZOOM,
        )
        pygame.draw.circle(
            self.screen,
            (255, 0, 0),
            self.mc2pc(self.mazeGame.end.x, self.mazeGame.end.y),
            5 * self.ZOOM,
        )
        pygame.draw.circle(
            self.screen,
            (0, 255, 0),
            self.mc2pc(self.mazeGame.robot_pos.x, self.mazeGame.robot_pos.y),
            5 * self.ZOOM,
        )

        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            self.mc2pc(self.mazeGame.robot_pos.x, self.mazeGame.robot_pos.y),
            self.mc2pc(self.mazeGame.robot_pos.x + self.mazeGame.robot_face[0] * 5, self.mazeGame.robot_pos.y + self.mazeGame.robot_face[1] * 5),
            1
        )

        if self.render_mode == "human":
            pygame.event.pump()
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )

    # game observation to environment observation
    def _go2eo(self, observation):
        return np.array(observation["sensor"] + [observation["end_direction"]], dtype=np.float32)

    #
    def _reward(self):
        new_distance = self.mazeGame.end.distance(self.mazeGame.robot_pos)
        move_reward = self.end_distance - new_distance
        return move_reward + self.TIME_PENALTY

    # math coordinate to pygame coordinate
    def mc2pc(self, x, y):
        return x * self.ZOOM, self.SCREEN_SIZE - y * self.ZOOM
