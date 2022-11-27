import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

home = "Mazes/"
maze = "maze_55"


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


def save_maze(file):
    start, end, maze_lines = parseFile(file)

    fig, ax = plt.subplots(figsize=[10, 10])

    ax.grid(True)

    for l in maze_lines:
        l = Line2D([l[0], l[2]], [l[1], l[3]], linewidth=1, color='k')
        ax.add_line(l)

    ax.scatter(start[0], start[1], color='r', edgecolors='k', s=550)
    ax.scatter(end[0], end[1], color='b', s=550, facecolors='none', edgecolors='k')

    ax.set_xticks([])
    ax.set_yticks([])

    plt.savefig(file + '.png', bbox_inches='tight')


if __name__ == '__main__':
    save_maze(home + maze)
