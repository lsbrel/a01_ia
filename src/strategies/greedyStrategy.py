import heapq


class GreedyStrategy:
    """
    Busca Gulosa (Greedy Best-First Search).

    Usa uma fila de prioridade (heap) para sempre expandir
    o nó com menor heurística (distância estimada até o objetivo).
    """

    def __init__(self, maze):
        self.maze = maze
        self.graph = self.maze.getGraph()

        self.visited = set()        # Nós já visitados (set para busca O(1))
        self.path = []              # Ordem de expansão dos nós
        self.came_from = {}         # Para reconstruir o caminho: nó → de onde veio
        self.totalCost = 0

        self.finishNode = list(self.graph.nodes(data=True))[-1]

    def run(self):
        # Nó inicial
        start = list(self.graph.nodes(data=True))[0]
        self.came_from[start[0]] = None  # Nó inicial não tem pai

        # Contador para desempate quando dois nós têm a mesma heurística
        counter = 0

        # Heap: (heurística, contador, node_id, node_data)
        heap = []
        heapq.heappush(heap, (0, counter, start[0], start[1]))

        while heap:
            _, _, node_id, node_data = heapq.heappop(heap)

            if node_id in self.visited:
                continue

            # Marca o nó como visitado e registra na ordem de expansão
            self.visited.add(node_id)
            self.path.append(node_id)

            # Chegou no destino
            if self.__isFinish((node_id, node_data)):
                return

            # Explora vizinhos
            for neighbor_id in self.graph.neighbors(node_id):
                neighbor = self.graph.nodes[neighbor_id]

                if self.__isWall(neighbor):
                    continue

                if neighbor_id not in self.visited:
                    # Registra de onde cada vizinho foi alcançado (apenas na primeira vez)
                    if neighbor_id not in self.came_from:
                        self.came_from[neighbor_id] = node_id

                    h = self.__manhattanDistance(neighbor, self.finishNode[1])
                    counter += 1
                    heapq.heappush(heap, (h, counter, neighbor_id, neighbor))

    def getResolutionPath(self):
        # Reconstrói o caminho do início ao fim percorrendo came_from de trás pra frente
        finish_id = self.finishNode[0]

        path = []
        current = finish_id
        while current is not None:
            path.append(current)
            current = self.came_from.get(current)
        path.reverse()

        # Calcula o custo real somando apenas os nós que fazem parte do caminho
        self.totalCost = sum(self.graph.nodes[n]["cost"] for n in path)

        print(f"Nós expandidos (busca gulosa): {len(self.path)}")
        print(f"Sequência de expansão: {self.path}")
        print(f"Caminho encontrado: {path}")
        print(f"Custo do caminho para busca gulosa: {self.totalCost}")
        return path

    def getExpansionOrder(self):
        # Retorna a lista de nós na ordem em que foram expandidos durante a busca
        return self.path

    def __isWall(self, node):
        return node["terrain"] == "#"

    def __isFinish(self, node):
        return node[1]["terrain"] == "F"

    def __manhattanDistance(self, currentNode, goalNode):
        # Distância de Manhattan: soma das diferenças absolutas das coordenadas x e y
        x = abs(goalNode["coordinates"][0] - currentNode["coordinates"][0])
        y = abs(goalNode["coordinates"][1] - currentNode["coordinates"][1])
        return x + y
