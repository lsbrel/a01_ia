import heapq


class AStarStrategy:
    """
    Algoritmo A*
    """

    def __init__(self, maze):
        # Guarda labirinto e gera o grafo a partir dele
        self.maze = maze
        self.graph = self.maze.getGraph()
        # Guarda nós já visitado
        self.visited = []
        # Menor custo real
        self.g_cost = {}
        # Guarda caminho que veio
        self.came_from = {}
        # Acho final?
        self.finishFound = False
        # Guarda custo final do caminho
        self.totalCost = 0

    def run(self):
        # Nó inicial e final
        startNode = list(self.graph.nodes(data=True))[0]
        finishNode = list(self.graph.nodes(data=True))[-1]

        # Custo inicial basicamente custo do primeiro nó
        self.g_cost[startNode[0]] = startNode[1]["cost"]
        # Nó inicial não tem pai
        self.came_from[startNode[0]] = None

        # Contador para desempate quando dois nós têm o mesmo valor somando caminho percorrido e caminho faltando, desempata quem chego antes
        counter = 0

        # Fila de prioridade
        heap = []
        # Calcula distancia ate o fim
        h0 = self.__manhattanDistance(startNode[1], finishNode[1])

        # mandamos a fila, custo pra chegar ate o no q tá + custo pra chega ate o fim, desempate e dados do nó 
        heapq.heappush(heap, (self.g_cost[startNode[0]] + h0, counter, startNode[0], startNode[1]))

        # Enqaunto tiver caminho para explorar
        while heap and not self.finishFound:
            # Pega melhor nó, menor g+h (caminho percorrido + caminho q falta)
            f, _, current_id, current_data = heapq.heappop(heap)

            # Ignora repetido
            if current_id in self.visited:
                continue

            # Marca como visitado
            self.visited.append(current_id)

            # Chegou no destino, para
            if self.__isFinish((current_id, current_data)):
                self.finishFound = True
                break

            # Olha caminhos possiveis
            for n in self.graph.neighbors(current_id):
                # pega dados do vizinho
                content = self.graph.nodes(data=True)[n]

                # Ignora paredes
                if self.__isWall(content):
                    continue

                # Ignora nós já expandidos
                if n in self.visited:
                    continue

                # quanto custa pra chegar nesse vizinho
                tentative_g = self.g_cost[current_id] + content["cost"]

                # Se o caminho atual for melhor em custo doq o caminho que tinhamos antes troca
                if n not in self.g_cost or tentative_g < self.g_cost[n]:
                    # Atualiza melhor caminho
                    self.g_cost[n] = tentative_g
                    self.came_from[n] = current_id

                    # f(n) = g(n) + h(n)
                    # Calcula custo ate o final
                    h = self.__manhattanDistance(content, finishNode[1])
                    # Soma com custo que levou pra chegar
                    f_score = tentative_g + h

                    # Numero de desempate caso mesmo custo
                    counter += 1
                    # Coloca na fila
                    heapq.heappush(heap, (f_score, counter, n, dict(content)))

    def getResolutionPath(self):
        # Reconstrói o caminho do início ao fim percorrendo came_from de trás pra frente
        finishNode = list(self.graph.nodes(data=True))[-1]
        finish_id = finishNode[0]

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

        # Calcula o custo real do caminho ótimo
        self.totalCost = self.g_cost.get(finish_id, 0)

        print(f"Nós expandidos (busca em A*): {len(self.visited)}")
        print(f"Sequência de expansão: {self.visited}")
        print(f"Caminho ótimo: {path}")
        print(f"Custo do caminho ótimo para busca em A*: {self.totalCost}")

        return path

    # Retorna a lista de nós na ordem em que foram expandidos durante a busca
    def getExpansionOrder(self):
        return self.visited

    # Se o terreno for # é parede
    def __isWall(self, node):
        return node["terrain"] == "#"

    # Se o terreno for F é o final
    def __isFinish(self, node):
        return node[1]["terrain"] == "F"

    # Distância de Manhattan soma das diferenças absolutas das coordenadas x e y
    def __manhattanDistance(self, currentNode, goalNode):
        x = abs(currentNode["coordinates"][0] - goalNode["coordinates"][0])
        y = abs(currentNode["coordinates"][1] - goalNode["coordinates"][1])
        return x + y
