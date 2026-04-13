from collections import deque

class DepthFirstSearchStrategy:
    """
    Busca em Profundidade
    """

    def __init__(self, maze):
         # Guarda labirinto e gera o grafo a partir dele
        self.maze = maze
        self.graph = self.maze.getGraph()

        # Guarda nós já visitado
        self.visited = []
        # Guarda caminho que veio
        self.came_from = {}
        # Guarda custo final do caminho
        self.totalCost = 0

    def run(self):
        #  Pega o primeiro nó da lista
        startNode = list(self.graph.nodes(data=True))[0]

        # Cria a pilha
        nodesToVisit = deque()
        # Adiciona o primeiro nó na pilha
        nodesToVisit.append(startNode)
        # Nó inicial não tem pai
        self.came_from[startNode[0]] = None

        # Enquanto tiver caminho na pilha continua
        while len(nodesToVisit) != 0:
            # pega o ultimo nó que entrou, continua do caminho mais recente smp
            current = nodesToVisit.pop()

            # Ja visitou ignora
            if current[0] in self.visited:
                continue

            # Ignora parede
            if self.__isWall(current):
                continue

            # Marca como visitado
            self.visited.append(current[0])

            # Pega caminhos vizinhos possiveis
            neighbors = list(self.graph.neighbors(current[0]))

            # Chegou no destino, para
            if self.__isFinish(current):
                break

            # pra cada vizinho
            for i in neighbors:
                # Marca de onde veio caso seja primeira vez
                if i not in self.came_from:
                    self.came_from[i] = current[0]
                # Coloca vizinho na pilha
                nodesToVisit.append((i, self.graph.nodes[i]))

    def getResolutionPath(self):
        # Pega o ultimo nó da lista
        finishNode = list(self.graph.nodes(data=True))[-1]
        finish_id = finishNode[0]

        # caminho
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

        print(f"Nós expandidos (busca em profundidade): {len(self.visited)}")
        print(f"Sequência de expansão: {self.visited}")
        print(f"Caminho encontrado: {path}")
        print(f"Custo do caminho para busca em profundidade: {self.totalCost}")
        return path

    # Retorna a lista de nós na ordem em que foram expandidos durante a busca
    def getExpansionOrder(self):
        return self.visited

    # Se o terreno for # é parede
    def __isWall(self, node):
        return node[1]["terrain"] == "#"

    # Se o terreno for F é o final
    def __isFinish(self, node):
        return node[1]["terrain"] == "F"
