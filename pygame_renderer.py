import pygame
from mazeGame import MazeGame
import sys

ZOOM = 4
SIZE = 200 * ZOOM


pygame.init()

screen = pygame.display.set_mode((SIZE, SIZE))

pygame.display.set_caption('maze navigation')


# math coordinate to pygame coordinate
def mc2pc(x, y):
    return x * ZOOM, SIZE - y * ZOOM


def fresh(env):
    screen.fill((255, 255, 255))
    for line in env.maze_lines:
        pygame.draw.line(screen, (0, 0, 0), mc2pc(*line[:2]), mc2pc(*line[2:]), 1)
    pygame.draw.circle(screen, (255, 0, 0), mc2pc(env.start.x, env.start.y), 5 * ZOOM)
    pygame.draw.circle(screen, (0, 255, 0), mc2pc(env.end.x, env.end.y), 5 * ZOOM)
    pygame.draw.circle(screen, (0, 0, 255), mc2pc(env.robot_pos.x, env.robot_pos.y), 5 * ZOOM)

    pygame.draw.line(screen, (255, 255, 255), mc2pc(env.robot_pos.x, env.robot_pos.y), mc2pc(env.robot_pos.x + env.robot_face[0] * 5, env.robot_pos.y + env.robot_face[1] * 5), 1)
    pygame.display.update()


if __name__ == '__main__':

    env = MazeGame(32)

    while True:

        # 循环获取事件，监听事件状态
        for event in pygame.event.get():
            # 判断用户是否点了"X"关闭按钮,并执行if代码段
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    env.action(2)
                elif event.key == pygame.K_DOWN:
                    env.action(3)
                elif event.key == pygame.K_LEFT:
                    env.action(0)
                elif event.key == pygame.K_RIGHT:
                    env.action(1)

                print(env.observation())

            if event.type == pygame.QUIT:
                # 卸载所有模块
                pygame.quit()
                # 终止程序，确保退出程序
                sys.exit()


        fresh(env)
        pygame.display.flip()  # 更新屏幕内容
