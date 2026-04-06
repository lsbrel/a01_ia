from collections import deque


class BreadthFirstSearchStrategy:
    """
    Busca em Largura

    Explora o labirinto nível por nível: visita todos os vizinhos do nó atual
    antes de avançar para os vizinhos dos vizinhos.
    """

    def __init__(self, maze):
        self.maze = maze # Labirinto com o grafo e a matriz
        self.visited = [] # Lista de nós visitados na ordem de exploração

    def run(self):
        graph = self.maze.getGraph() # Obtém o grafo do labirinto

        # Fila de nós a visitar — começa pelo primeiro nó (canto superior esquerdo)
        nodesToVist = deque() # Cria lista otimizada para inserção e remoção de elementos
        nodesToVist.append(list(graph.nodes(data=True))[0]) # Adiciona o primeiro nó na lista

        while len(nodesToVist) != 0:
            # Retira o nó mais antigo da fila
            # O primeiro nó adicionado será o próximo a ser explorado
            current = nodesToVist.popleft() # Remove o primeiro nó da lista

            # Só processa se ainda não visitou este nó (nó pode ter sido visitado em outro caminho)
            if current[0] not in self.visited:

                # Ignora paredes não podem ser atravessadas
                if self.__isWall(current):
                    continue

                # Marca o nó como visitado
                self.visited.append(current[0])
                neighbors = list(graph.neighbors(current[0]))

                # Se chegou ao destino, para a busca
                if self.__isFinish(current):
                    break

                # Adiciona todos os vizinhos a fila para serem explorados depois
                for i in neighbors:
                    nodesToVist.append((i, graph.nodes[i]))

    def getResolutionPath(self):
        # Retorna a lista de nós visitados (o caminho percorrido pela busca)
        return self.visited

    def __isWall(self, node):
        # Verifica se o nó é uma parede ("#")
        return node[1]["terrain"] == "#"

    def __isFinish(self, node):
        # Verifica se o nó é o destino final ("F")
        return node[1]["terrain"] == "F"
