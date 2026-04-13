import heapq


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

    def run(self):
        startNode = list(self.graph.nodes(data=True))[0]
        finishNode = list(self.graph.nodes(data=True))[-1]

        # Inicializa o nó inicial com g = seu próprio custo (ou 0, dependendo da convenção)
        self.g_cost[startNode[0]] = startNode[1]["cost"]
        self.came_from[startNode[0]] = None

        # Contador para desempate quando dois nós têm o mesmo f(n)
        counter = 0

        # Heap: (f(n), contador, node_id, node_data) — O(log n) por inserção e remoção
        heap = []
        h0 = self.__manhattanDistance(startNode[1], finishNode[1])
        heapq.heappush(heap, (self.g_cost[startNode[0]] + h0, counter, startNode[0], startNode[1]))

        while heap and not self.finishFound:
            # Retira o nó com menor f da heap — O(log n)
            f, _, current_id, current_data = heapq.heappop(heap)

            # Pula se já foi expandido (pode estar duplicado na heap)
            if current_id in self.visited:
                continue

            # Marca como expandido
            self.visited.append(current_id)

            # Se chegou ao destino, para a busca
            if self.__isFinish((current_id, current_data)):
                self.finishFound = True
                break

            # Explora vizinhos
            for n in self.graph.neighbors(current_id):
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

                    # f(n) = g(n) + h(n)
                    h = self.__manhattanDistance(content, finishNode[1])
                    f_score = tentative_g + h

                    counter += 1
                    heapq.heappush(heap, (f_score, counter, n, dict(content)))

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

        print(f"Nós expandidos (busca em A*): {len(self.visited)}")
        print(f"Sequência de expansão: {self.visited}")
        print(f"Caminho ótimo: {path}")
        print(f"Custo do caminho ótimo para busca em A*: {self.totalCost}")

        return path

    def getExpansionOrder(self):
        # Retorna a lista de nós na ordem em que foram expandidos durante a busca
        return self.visited

    def __isWall(self, node):
        return node["terrain"] == "#"

    def __isFinish(self, node):
        return node[1]["terrain"] == "F"

    def __manhattanDistance(self, currentNode, goalNode):
        x = abs(currentNode["coordinates"][0] - goalNode["coordinates"][0])
        y = abs(currentNode["coordinates"][1] - goalNode["coordinates"][1])
        return x + y
