import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation


class MazeResolutionAnimation:

    def __init__(self, maze, path):
        self.maze = maze
        self.path = path
        self.terrains = {
            "#": "gray",
            "G": "green",
            "L": "brown",
            "I": "tab:blue",
            "F": "tab:blue",
        }
        self.colors = [
            self.terrains[node[1]["terrain"]] for node in self.maze.nodes(data=True)
        ]
        self.fig, self.ax = plt.subplots()
        self.layout = nx.bfs_layout(self.maze, start=0)

    def run(self):
        nx.draw(
            self.maze,
            pos=self.layout,
            ax=self.ax,
            with_labels=True,
            node_color=self.colors,
        )
        self.anim = animation.FuncAnimation(
            self.fig,
            self.__animate,
            frames=len(self.path),
            interval=1000,
            init_func=self.__initAnimation,
            repeat=False,
        )
        plt.show()

    def __initAnimation(self):
        pass

    def __animate(self, frame):
        if frame < len(self.path):
            self.ax.clear()
            normalizedIndex = list(self.maze.nodes).index(self.path[frame])
            self.colors[normalizedIndex] = "orange"
            nx.draw(
                self.maze,
                pos=self.layout,
                ax=self.ax,
                with_labels=True,
                node_color=self.colors,
            )
