from collections import deque


class DepthFirstSearchStrategy:
    """
    Busca em Profundidade

    Explora o labirinto seguindo um caminho até o fim antes de voltar e tentar outro.
    """

    def __init__(self, maze):
        self.maze = maze                # Labirinto com o grafo e a matriz
        self.graph = self.maze.getGraph()  # Grafo do labirinto
        self.visited = []               # Lista de nós visitados na ordem de exploração
        self.came_from = {}             # Para reconstruir o caminho: nó → de onde veio
        self.totalCost = 0

    def run(self):
        startNode = list(self.graph.nodes(data=True))[0]

        # Pilha de nós a visitar — começa pelo primeiro nó (canto superior esquerdo)
        nodesToVisit = deque()  # Cria lista otimizada para inserção e remoção de elementos
        nodesToVisit.append(startNode)
        self.came_from[startNode[0]] = None  # Nó inicial não tem pai

        # Enquanto a lista não estiver vazia, continua a busca
        while len(nodesToVisit) != 0:
            # Retira o nó do topo da pilha
            # O último nó adicionado será o próximo a ser explorado
            current = nodesToVisit.pop()  # Remove o último nó da lista

            # Só processa se ainda não visitou este nó (nó pode ter sido visitado em outro caminho)
            if current[0] in self.visited:
                continue

            # Ignora paredes não podem ser atravessadas
            if self.__isWall(current):
                continue

            # Marca o nó como visitado
            self.visited.append(current[0])

            neighbors = list(self.graph.neighbors(current[0]))

            # Se chegou ao destino, para a busca
            if self.__isFinish(current):
                break

            # Empilha os vizinhos o último adicionado será o próximo a ser explorado
            for i in neighbors:
                # Registra de onde cada vizinho foi alcançado (apenas na primeira vez)
                if i not in self.came_from:
                    self.came_from[i] = current[0]
                nodesToVisit.append((i, self.graph.nodes[i]))

    def getResolutionPath(self):
        # Reconstrói o caminho do início ao fim percorrendo came_from de trás pra frente
        finishNode = list(self.graph.nodes(data=True))[-1]
        finish_id = finishNode[0]

        path = []
        current = finish_id
        while current is not None:
            path.append(current)
            current = self.came_from.get(current)
        path.reverse()

        # Calcula o custo real somando apenas os nós que fazem parte do caminho
        self.totalCost = sum(self.graph.nodes[n]["cost"] for n in path)

        print(f"Nós expandidos (busca em profundidade): {len(self.visited)}")
        print(f"Sequência de expansão: {self.visited}")
        print(f"Caminho encontrado: {path}")
        print(f"Custo do caminho para busca em profundidade: {self.totalCost}")
        return path

    def getExpansionOrder(self):
        # Retorna a lista de nós na ordem em que foram expandidos durante a busca
        return self.visited

    def __isFinish(self, node):
        # Verifica se o nó é o destino final ("F")
        return node[1]["terrain"] == "F"

    def __isWall(self, node):
        # Verifica se o nó é uma parede ("#")
        return node[1]["terrain"] == "#"
