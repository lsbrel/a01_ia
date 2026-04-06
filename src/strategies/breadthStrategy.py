from collections import deque


class BreadthFirstSearchStrategy:

    def __init__(self, maze):
        self.maze = maze
        self.visited = []

    def run(self):
        graph = self.maze.getGraph()

        nodesToVist = deque()
        nodesToVist.append(list(graph.nodes(data=True))[0])

        while len(nodesToVist) != 0:
            current = nodesToVist.popleft()
            if current[0] not in self.visited:

                if self.__isWall(current):
                    continue

                self.visited.append(current[0])
                neighbors = list(graph.neighbors(current[0]))

                if self.__isFinish(current):
                    break

                for i in neighbors:
                    nodesToVist.append((i, graph.nodes[i]))

    def getResolutionPath(self):
        return self.visited

    def __isWall(self, node):
        return node[1]["terrain"] == "#"

    def __isFinish(self, node):
        return node[1]["terrain"] == "F"
