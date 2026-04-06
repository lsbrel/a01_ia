import numpy as np
import networkx as nx


class MazeBuilder:

    def __init__(self, size: int, walls: int):
        self.size = size
        self.walls = walls
        self.boostrap()

    def boostrap(self):
        self.terrains = {
            "#": "gray",
            "G": "green",
            "L": "brown",
            "I": "tab:blue",
            "F": "tab:blue",
        }
        self.costs = {"#": 0, "G": 1, "L": 5, "I": 0, "F": 0}
        self.places = ["G", "L"]
        self.initialPositions = [0, 0]
        self.finalPosition = [self.size - 1, self.size - 1]

    def createMaze(self):
        self.matrix = np.random.choice(self.places, size=(self.size, self.size))
        self.__defineWalls()
        self.__defineStartAndFinish()
        self.__defineGraph()

    def __defineStartAndFinish(self):
        self.matrix[0][0] = "I"
        self.matrix[self.size - 1][self.size - 1] = "F"

    def __defineWalls(self):
        for wall in range(self.walls):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.matrix[x, y] = "#"

    def __defineGraph(self):
        self.maze = nx.Graph()

        self.matrixFlat = self.matrix.flatten()
        firstRow = len(self.matrix) - 1
        lastRow = len(self.matrix) * (len(self.matrix) - 1)
        firstColumn = [
            index
            for index, num in enumerate(range(len(self.matrixFlat)))
            if index % self.size == 0
        ]
        lastColumn = [
            index + (self.size - 1)
            for index, _ in enumerate(range(len(self.matrixFlat)))
            if index % self.size == 0
        ]

        for index, value in enumerate(self.matrixFlat):
            if self.__isWall(index):
                continue
            if index > firstRow:
                if not self.__isWall(index - self.size):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index - self.size,
                        terrain=self.matrixFlat[index - self.size],
                        cost=self.costs[self.matrixFlat[index - self.size]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index - self.size)

            if index < lastRow:
                if not self.__isWall(index + self.size):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index + self.size,
                        terrain=self.matrixFlat[index + self.size],
                        cost=self.costs[self.matrixFlat[index + self.size]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index + self.size)

            if index not in firstColumn:
                if not self.__isWall(index - 1):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index - 1,
                        terrain=self.matrixFlat[index - 1],
                        cost=self.costs[self.matrixFlat[index - 1]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index - 1)

            if index not in lastColumn:
                if not self.__isWall(index + 1):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.matrixFlat[index],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index + 1,
                        terrain=self.matrixFlat[index + 1],
                        cost=self.matrixFlat[index + 1],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index + 1)

    def __positionExists(self, pos):
        return 0 <= pos <= self.matrix.shape[0]

    def __isWall(self, pos):
        return False  # caso retorne falso monta grafo com as paredes também
        return self.matrixFlat[pos] == "#"

    def __resolveCoordinates(self, index):
        row = 0
        column = 0
        for i in range(1, index):
            if i % self.size == 0:
                row += 1
                column = 0

            column += 1
        return (row, column)

    def getGraph(self):
        return self.maze

    def getMatrix(self):
        return self.matrix

    def showMatrix(self):
        print(self.matrix)
