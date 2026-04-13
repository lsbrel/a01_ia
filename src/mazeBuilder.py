import numpy as np
import networkx as nx


class MazeBuilder:

    def __init__(self, size: int, walls: int, visibleWalls: bool):
        # Tamanho do labirinto
        self.size = size
        # Quantidade de paredes
        self.walls = walls
        # Visivel as paredes
        self.visibleWalls = visibleWalls
        self.boostrap()

    def boostrap(self):
        # Mapeamento de cada tipo de terreno para sua cor na animação
        self.terrains = {
            "#": "gray",
            "G": "green",
            "C": "lightgray",
            "L": "brown",
            "I": "tab:blue",
            "F": "tab:blue",
        }

        # Custo de movimento por tipo de terreno
        self.costs = {"#": 0, "G": 1, "C": 4, "L": 5, "I": 0, "F": 0}

        # Terrenos que podem aparecer aleatoriamente
        self.places = ["G", "C", "L"]

        # Posição inicial
        self.initialPositions = [0, 0]

        # Posição final
        self.finalPosition = [self.size - 1, self.size - 1]

    def createMaze(self):
        # Preenche a grade com terrenos aleatórios
        self.matrix = np.random.choice(self.places, size=(self.size, self.size))

        # Define as paredes, início, fim e depois monta o grafo
        self.__defineWalls()
        self.__defineStartAndFinish()
        self.__defineGraph()

    def __defineStartAndFinish(self):
        # Marca a célula [0][0] como início e a última célula como fim
        self.matrix[0][0] = "I"
        self.matrix[self.size - 1][self.size - 1] = "F"

    def __defineWalls(self):
        # Insere paredes em posições aleatórias da grade
        for wall in range(self.walls):
            x = np.random.randint(0, self.size)
            y = np.random.randint(0, self.size)
            self.matrix[x, y] = "#"

    def __defineGraph(self):
        # Cria um grafo onde cada célula do labirinto é um nó
        self.maze = nx.Graph()

        # Transforma a matriz 2D em uma lista linear para facilitar o acesso por índice
        self.matrixFlat = self.matrix.flatten()

        # Índice da última célula da primeira linha
        firstRow = len(self.matrix) - 1

        # Índice da primeira célula da última linha
        lastRow = len(self.matrix) * (len(self.matrix) - 1)

        # Índices das células na primeira coluna não têm vizinho na esquerda
        firstColumn = [
            index
            for index, num in enumerate(range(len(self.matrixFlat)))
            if index % self.size == 0
        ]

        # Índices das células na última coluna não têm vizinho na direita
        lastColumn = [
            index + (self.size - 1)
            for index, _ in enumerate(range(len(self.matrixFlat)))
            if index % self.size == 0
        ]

        # Percorre cada célula da matriz linearizada para criar nós e arestas no grafo
        for index, value in enumerate(self.matrixFlat):
             # Pula paredes
            if self.__isWall(index):
                continue

            # Tenta conectar com a célula de cima (índice - size)
            if index > firstRow:
                if not self.__isWall(index - self.size):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index - self.size,
                        terrain=self.matrixFlat[index - self.size],
                        cost=self.costs[self.matrixFlat[index - self.size]],
                        coordinates=self.__resolveCoordinates(index - self.size),
                    )
                    self.maze.add_edge(index, index - self.size)

            # Tenta conectar com a célula de baixo
            if index < lastRow:
                if not self.__isWall(index + self.size):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index + self.size,
                        terrain=self.matrixFlat[index + self.size],
                        cost=self.costs[self.matrixFlat[index + self.size]],
                        coordinates=self.__resolveCoordinates(index + self.size),
                    )
                    self.maze.add_edge(index, index + self.size)

            # Tenta conectar com a célula à esquerda
            if index not in firstColumn:
                if not self.__isWall(index - 1):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index - 1,
                        terrain=self.matrixFlat[index - 1],
                        cost=self.costs[self.matrixFlat[index - 1]],
                        coordinates=self.__resolveCoordinates(index - 1),
                    )
                    self.maze.add_edge(index, index - 1)

            # Tenta conectar com a célula à direita
            if index not in lastColumn:
                if not self.__isWall(index + 1):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.costs[self.matrixFlat[index]],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index + 1,
                        terrain=self.matrixFlat[index + 1],
                        cost=self.costs[self.matrixFlat[index + 1]],
                        coordinates=self.__resolveCoordinates(index + 1),
                    )
                    self.maze.add_edge(index, index + 1)

    def __isWall(self, pos):
        # Se visibleWalls=True, paredes entram
        # Se visibleWalls=False, paredes são excluídas
        if self.visibleWalls:
            return False
        else:
            return self.matrixFlat[pos] == "#"

    def __resolveCoordinates(self, index):
        # Converte um índice linear para coordenadas (linha, coluna) na grade
        return (index // self.size, index % self.size)

    def getGraph(self):
        # Retorna o grafo montado do labirinto
        return self.maze

    def getMatrix(self):
        # Retorna a matriz 2D do labirinto
        return self.matrix

    def showMatrix(self):
        # Imprime a matriz do labirinto
        print(self.matrix)

    def showLegend(self):
        # Exibe a legenda dos tipos de terreno
        print("\n=== Legenda ===")
        print("  I = Início   (custo  0)")
        print("  F = Fim      (custo  0)")
        print("  G = Grama    (custo  1)")
        print("  C = Calçada  (custo  4)")
        print("  L = Lama     (custo  5)")
        print("  # = Parede\n")
