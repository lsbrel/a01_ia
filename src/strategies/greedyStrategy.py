import heapq

class GreedyStrategy:
    """
    Busca Gulosa
    """

    def __init__(self, maze):
        # Guarda labirinto e gera o grafo a partir dele
        self.maze = maze
        self.graph = self.maze.getGraph()

        # Guarda nós já visitado em set pq é mais rapido checagem
        self.visited = set()
        # Guarda ordem explorada
        self.path = []
        # Guarda caminho que veio
        self.came_from = {}
        # Guarda custo final do caminho
        self.totalCost = 0
        # Pega o ultimo nó da lista e assume que é o final do caminho
        self.finishNode = list(self.graph.nodes(data=True))[-1]

    def run(self):
        #  Pega o primeiro nó da lista
        start = list(self.graph.nodes(data=True))[0]
        # Nó inicial não tem pai
        self.came_from[start[0]] = None

        # Desempatar quando dois nós parecem igualmente bons
        counter = 0

        # Cria fila de prioridade
        heap = []
        # Coloca o ponto inicial na fila (heuristica, desempate, id, dados)
        heapq.heappush(heap, (0, counter, start[0], start[1]))

        # Loop pra enquanto tiver caminho pra explorar
        while heap:
            # Pega melhor nó, aquele q parece mais perto do F
            _, _, node_id, node_data = heapq.heappop(heap)

            # Ja visitou ignora
            if node_id in self.visited:
                continue

            # Marca como visitado e guarda que passou ali
            self.visited.add(node_id)
            self.path.append(node_id)

            # Chegou no destino, para
            if self.__isFinish((node_id, node_data)):
                return

            # Explora vizinhos de caminho possivel
            for neighbor_id in self.graph.neighbors(node_id):
                # Pega o proximo vizinho
                neighbor = self.graph.nodes[neighbor_id]

                # se vizinho for parede ignora
                if self.__isWall(neighbor):
                    continue

                # se ainda não foi visitado
                if neighbor_id not in self.visited:
                    # Marca de onde veio caso seja primeira vez
                    if neighbor_id not in self.came_from:
                        self.came_from[neighbor_id] = node_id

                    # Usa manhattan para definir quao perto esse vizinho esta do final
                    h = self.__manhattanDistance(neighbor, self.finishNode[1])
                    # atualiza o desempate
                    counter += 1

                    # Coloca vizinho na fila
                    heapq.heappush(heap, (h, counter, neighbor_id, neighbor))

    def getResolutionPath(self):
        # Reconstrói o caminho do início ao fim percorrendo came_from de trás pra frente
        finish_id = self.finishNode[0]
        # Caminho
        path = []
        # Começa do fim
        current = finish_id
        # Volta até o inicio
        while current is not None:
            path.append(current)
            current = self.came_from.get(current)

        # Inverte o array para ficar do inicio ao fim
        path.reverse()

        # Somaa custo do caminho
        self.totalCost = sum(self.graph.nodes[n]["cost"] for n in path)

        print(f"Nós expandidos (busca gulosa): {len(self.path)}")
        print(f"Sequência de expansão: {self.path}")
        print(f"Caminho encontrado: {path}")
        print(f"Custo do caminho para busca gulosa: {self.totalCost}")
        return path

    # Retorna a lista de nós na ordem em que foram expandidos durante a busca
    def getExpansionOrder(self):
        return self.path

    # Se o terreno for # é parede
    def __isWall(self, node):
        return node["terrain"] == "#"

    # Se o terreno for F é o final
    def __isFinish(self, node):
        return node[1]["terrain"] == "F"

    # Distância de Manhattan soma das diferenças absolutas das coordenadas x e y
    def __manhattanDistance(self, currentNode, goalNode):
        x = abs(goalNode["coordinates"][0] - currentNode["coordinates"][0])
        y = abs(goalNode["coordinates"][1] - currentNode["coordinates"][1])
        return x + y
