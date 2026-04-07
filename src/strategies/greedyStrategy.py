import math


class GreedyStrategy:
    """
    Busca Gulosa (Greedy Best-First Search).

    A cada passo, escolhe o vizinho com o menor custo de terreno,
    sem considerar o custo acumulado do caminho percorrido.
    Usa recursão para explorar os nós.
    """

    def __init__(self, maze):
        self.maze = maze  # Labirinto com o grafo e a matriz
        self.graph = self.maze.getGraph()  # Obtém o grafo do labirinto
        self.visited = []  # Lista de nós visitados na ordem de exploração
        self.finishFound = False  # Flag para parar a recursão ao encontrar o destino
        self.totalCost = 0
        self.finishNode = list(self.graph.nodes(data=True))[-1]

    def run(self, current=None):
        # Na primeira chamada, começa pelo primeiro nó do grafo (canto superior esquerdo)
        if current is None:
            current = list(self.graph.nodes(data=True))[0]

        # Pega os índices dos vizinhos do nó atual
        nAux = list(self.graph.neighbors(current[0]))

        # Marca o nó atual como visitado se o destino ainda não foi encontrado
        if not self.finishFound:
            self.visited.append(current[0])
            self.totalCost += current[1]["cost"]

        # Se chegou ao destino, para a recursão
        if self.__isFinish(current):
            return

        # Filtra os vizinhos removendo paredes e monta a lista de vizinhos válidos
        neighbors = []
        for i in nAux:
            node = self.graph.nodes[i]
            if self.__isWall(node):
                continue
            neighbors.append((i, self.graph.nodes[i]))

        # Ordena os vizinhos pelo custo do terreno (menor custo primeiro)
        neighbors = sorted(
            neighbors,
            key=lambda n: int(self.__euclideanDistance(n[1], self.finishNode[1])),
        )

        # Visita os vizinhos em ordem de custo, de forma recursiva, se ainda não foram visitados
        for n in neighbors:
            if n[0] not in self.visited:
                self.run(current=n)

    def getResolutionPath(self):
        # Retorna a lista de nós visitados (o caminho percorrido pela busca)
        print(f"Nós expandidos para busca em gulosa: {self.visited}")
        print(f"Custo do caminho expandidos para busca em gulosa: {self.totalCost}")
        return self.visited

    def __isWall(self, node):
        # Verifica se o nó é uma parede ("#")
        return node["terrain"] == "#"

    def __isFinish(self, node):
        # Verifica se o nó é o destino ("F")
        # Se for, ativa a flag para parar a recursão
        if self.finishFound or node[1]["terrain"] == "F":
            self.finishFound = True
            return True
        else:
            return False

    def __manhattanDistance(self, currentNode, goalNode):
        x = abs(currentNode["coordinates"][0] - goalNode["coordinates"][0])
        y = abs(currentNode["coordinates"][1] - goalNode["coordinates"][1])
        return x + y

    def __euclideanDistance(self, currentNode, goalNode):
        x = (goalNode["coordinates"][0] - currentNode["coordinates"][0]) ** 2
        y = (goalNode["coordinates"][1] - currentNode["coordinates"][1]) ** 2
        return math.sqrt(x + y)
