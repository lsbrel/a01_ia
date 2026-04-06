from collections import deque
import math


class AStarStrategy:
    """
    Algoritmo A* (A-estrela).

    Combina o custo real acumulado do caminho percorrido (g)
    com uma estimativa da distância até o destino (heurística h).
    A fórmula f = g + h garante que o A* encontre o caminho de menor custo.
    """

    def __init__(self, maze):
        self.maze = maze  # Labirinto com o grafo e a matriz
        self.graph = self.maze.getGraph()  # Obtém o grafo do labirinto
        self.visited = []  # Lista de nós visitados na ordem de exploração
        self.probabilityVisited = []  # (não utilizado atualmente)
        self.pathSum = 0  # Custo acumulado do caminho percorrido até agora (g)
        self.finishFound = False  # Flag para parar a busca ao encontrar o destino
        self.totalCost = 0  # Custo do caminho

    def run(self, current=None):
        # Fila de nós a explorar
        openList = deque()

        # Nó inicial e nó destino
        startNode = list(self.graph.nodes(data=True))[0]
        finishNode = list(self.graph.nodes(data=True))[-1]

        # Adiciona o nó inicial na fila
        openList.append(startNode)

        while len(openList) != 0 and not self.finishFound:
            # Retira o nó com menor f = g + h da fila
            current = openList.popleft()

            # Se chegou ao destino, para a busca
            if self.__isFinish(current):
                self.finishFound = True

            # Pega os índices dos vizinhos do nó atual
            neighbors = list(self.graph.neighbors(current[0]))
            for n in neighbors:
                content = self.graph.nodes(data=True)[n]

                # Ignora paredes
                if self.__isWall(content):
                    continue

                # Ignora nós que já foram visitados
                if n in self.visited:
                    self.pathSum -= content["cost"]
                    continue

                # Adiciona o nó na fila
                openList.append((n, content))

            # Reordena a fila pelo valor de f (custo real + estimativa) para cada nó candidato
            # O próximo a ser processado será sempre o de menor f
            openList = deque(
                sorted(
                    openList,
                    key=lambda n: self.__heuristics(current=n[1], finish=finishNode[1]),
                )
            )

            # Marca o nó atual como visitado e acumula o custo do terreno
            self.visited.append(current[0])
            self.totalCost += current[1]["cost"]
            self.__actualDistance(current)

    def getResolutionPath(self):
        # Retorna a lista de nós visitados (o caminho percorrido pela busca)
        print(f"Nós expandidos para busca em A*: {self.visited}")
        print(f"Custo do caminho expandidos para busca em A*: {self.totalCost}")
        return self.visited

    def __isWall(self, node):
        # Verifica se o nó é uma parede ("#")
        return node["terrain"] == "#"

    def __heuristics(self, current, finish):
        # f(n) = g(n) + h(n)
        # g(n) = custo acumulado do caminho percorrido até o nó atual
        # h(n) = distância de Manhattan estimada do nó atual até o destino
        actualDistance = self.pathSum + current["cost"]
        estimateDistance = self.__manhatanDistance(current, finish)
        return actualDistance + estimateDistance

    def __isFinish(self, node):
        # Verifica se o nó é o destino final ("F")
        return node[1]["terrain"] == "F"

    def __actualDistance(self, currentNode):
        # Acumula o custo do terreno do nó atual ao custo total do caminho
<<<<<<< HEAD
        self.pathSum = sum(self.visited)
=======
        # self.pathSum = sum(self.visite)
>>>>>>> 1cc7c070cf8c0b7c71d67e2abbe40295545a729a
        self.pathSum += int(currentNode[1]["cost"])

    def __euclideanDistance(self, currentNode, goalNode):
        # Distância euclidiana entre dois nós (reta entre dois pontos) nao ta em uso porque no nosso grid não é possivel movimentação em diagonais.
        x = (goalNode["coordinates"][0] - currentNode["coordinates"][0]) ** 2
        y = (goalNode["coordinates"][1] - currentNode["coordinates"][1]) ** 2
        return math.sqrt(x + y)

    def __manhatanDistance(self, currentNode, goalNode):
        # Distância de Manhattan: soma das diferenças absolutas de linha e coluna
        # Adequada para grades onde só se move em 4 direções (cima, baixo, esquerda, direita)
        x = abs(currentNode["coordinates"][0] - goalNode["coordinates"][0])
        y = abs(currentNode["coordinates"][1] - goalNode["coordinates"][1])
        return x + y
