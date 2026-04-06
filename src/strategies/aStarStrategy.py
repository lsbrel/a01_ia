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
        self.maze = maze
        self.graph = self.maze.getGraph()
        self.visited = []           # Nós expandidos na ordem de exploração
        self.g_cost = {}            # g(n): menor custo real do início até cada nó
        self.came_from = {}         # Para reconstruir o caminho ótimo
        self.finishFound = False
        self.totalCost = 0

    def run(self, current=None):
        openList = deque()

        startNode = list(self.graph.nodes(data=True))[0]
        finishNode = list(self.graph.nodes(data=True))[-1]

        # Inicializa o nó inicial com g = seu próprio custo (ou 0, dependendo da convenção)
        self.g_cost[startNode[0]] = startNode[1]["cost"]
        self.came_from[startNode[0]] = None

        # Cria cópia dos dados do nó inicial com pathCost
        start_data = dict(startNode[1])
        start_data["pathCost"] = startNode[1]["cost"]
        openList.append((startNode[0], start_data))

        while len(openList) != 0 and not self.finishFound:
            # Retira o nó com menor f da fila
            current = openList.popleft()
            current_id = current[0]

            # Pula se já foi expandido (pode estar duplicado na fila)
            if current_id in self.visited:
                continue

            # Marca como expandido
            self.visited.append(current_id)

            # Se chegou ao destino, para a busca
            if self.__isFinish(current):
                self.finishFound = True
                break

            # Explora vizinhos
            neighbors = list(self.graph.neighbors(current_id))
            for n in neighbors:
                content = self.graph.nodes(data=True)[n]

                # Ignora paredes
                if self.__isWall(content):
                    continue

                # Ignora nós já expandidos
                if n in self.visited:
                    continue

                # g(vizinho) = g(atual) + custo do vizinho
                tentative_g = self.g_cost[current_id] + content["cost"]

                # Só adiciona/atualiza se encontrou caminho melhor até este vizinho
                if n not in self.g_cost or tentative_g < self.g_cost[n]:
                    self.g_cost[n] = tentative_g
                    self.came_from[n] = current_id

                    # Cria cópia dos dados com pathCost individual
                    node_data = dict(content)
                    node_data["pathCost"] = tentative_g

                    openList.append((n, node_data))

            # Reordena a fila por f(n) = g(n) + h(n)
            openList = deque(
                sorted(
                    openList,
                    key=lambda n: self.__heuristics(current=n[1], finish=finishNode[1]),
                )
            )

    def getResolutionPath(self):
        """Reconstrói o caminho ótimo do início ao fim usando came_from."""
        # Encontra o nó final
        finishNode = list(self.graph.nodes(data=True))[-1]
        finish_id = finishNode[0]

        # Reconstrói o caminho de trás pra frente
        path = []
        current = finish_id
        while current is not None:
            path.append(current)
            current = self.came_from.get(current)
        path.reverse()

        # Calcula o custo real do caminho ótimo
        self.totalCost = self.g_cost.get(finish_id, 0)

        print(f"Nós expandidos para busca em A*: {self.visited}")
        print(f"Caminho ótimo: {path}")
        print(f"Custo do caminho ótimo para busca em A*: {self.totalCost}")

        return path  # Retorna o caminho ótimo, não todos os nós expandidos

    def __isWall(self, node):
        return node["terrain"] == "#"

    def __heuristics(self, current, finish):
        # f(n) = g(n) + h(n)
        actualDistance = current["pathCost"]
        estimateDistance = self.__manhattanDistance(current, finish)
        return actualDistance + estimateDistance

    def __isFinish(self, node):
        return node[1]["terrain"] == "F"

    def __manhattanDistance(self, currentNode, goalNode):
        x = abs(currentNode["coordinates"][0] - goalNode["coordinates"][0])
        y = abs(currentNode["coordinates"][1] - goalNode["coordinates"][1])
        return x + y