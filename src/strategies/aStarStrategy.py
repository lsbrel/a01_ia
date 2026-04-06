from collections import deque
import math


class AStarStrategy:

    def __init__(self, maze):
        self.maze = maze
        self.graph = self.maze.getGraph()
        self.visited = []
        self.probabilityVisited = []
        self.pathSum = 0
        self.finishFound = False

    def run(self, current=None):
        openList = deque()

        startNode = list(self.graph.nodes(data=True))[0]
        finishNode = list(self.graph.nodes(data=True))[-1]

        openList.append(startNode)

        while len(openList) != 0 and not self.finishFound:
            current = openList.popleft()
            if self.__isFinish(current):
                self.finishFound = True

            neighbors = list(self.graph.neighbors(current[0]))
            for n in neighbors:
                content = self.graph.nodes(data=True)[n]
                if self.__isWall(content):
                    continue

                if n in self.visited:
                    continue

                openList.append((n, content))

            openList = deque(
                sorted(
                    openList,
                    key=lambda n: self.__heuristics(current=n[1], finish=finishNode[1]),
                )
            )

            self.visited.append(current[0])
            self.__actualDistance(current)

    def getResolutionPath(self):
        return self.visited

    def __isWall(self, node):
        return node["terrain"] == "#"

    def __heuristics(self, current, finish):
        actualDistance = self.pathSum
        estimateDistance = self.__manhatanDistance(current, finish)
        return actualDistance + estimateDistance

    def __isFinish(self, node):
        return node[1]["terrain"] == "F"

    def __actualDistance(self, currentNode):
        self.pathSum += int(currentNode[1]["cost"])

    def __euclideanDistance(self, currentNode, goalNode):
        x = (goalNode["coordinates"][0] - currentNode["coordinates"][0]) ** 2
        y = (goalNode["coordinates"][1] - currentNode["coordinates"][1]) ** 2
        return math.sqrt(x + y)

    def __manhatanDistance(self, currentNode, goalNode):
        x = abs(currentNode["coordinates"][0] - goalNode["coordinates"][0])
        y = abs(currentNode["coordinates"][1] - goalNode["coordinates"][1])
        return x + y
