class GreedyStrategy:

    def __init__(self, maze):
        self.maze = maze
        self.graph = self.maze.getGraph()
        self.visited = []
        self.finishFound = False

    def run(self, current=None):
        if current is None:
            current = list(self.graph.nodes(data=True))[0]

        nAux = list(self.graph.neighbors(current[0]))

        if not self.finishFound:
            self.visited.append(current[0])

        if self.__isFinish(current):
            return

        neighbors = []
        for i in nAux:
            node = self.graph.nodes[i]
            if self.__isWall(node):
                continue

            neighbors.append((i, self.graph.nodes[i]))

        neighbors = sorted(neighbors, key=lambda n: int(n[1]["cost"]))
        for n in neighbors:
            if n[0] not in self.visited:
                self.run(current=n)

    def getResolutionPath(self):
        return self.visited

    def __isWall(self, node):
        return node["terrain"] == "#"

    def __isFinish(self, node):
        if self.finishFound or node[1]["terrain"] == "F":
            self.finishFound = True
            return True
        else:
            return False
