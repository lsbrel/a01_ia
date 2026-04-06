import numpy as np
import networkx as nx


class MazeBuilder:
    """
    Constrói o labirinto: gera a matriz com terrenos aleatórios,
    posiciona as paredes, define o início/fim e monta o grafo de conexões entre células.
    """

    def __init__(self, size: int, walls: int):
        self.size = size    # Tamanho do labirinto (ex: 5 → grade 5x5)
        self.walls = walls  # Quantidade de paredes a inserir aleatoriamente
        self.boostrap()

    def boostrap(self):
        # Mapeamento de cada tipo de terreno para sua cor na animação
        self.terrains = {
            "#": "gray",       # Parede — bloqueio, não pode passar
            "G": "green",      # Grama — custo baixo para atravessar
            "L": "brown",      # Lama — custo alto para atravessar
            "I": "tab:blue",   # Início (Initial) — ponto de partida
            "F": "tab:blue",   # Fim (Finish) — destino a alcançar
        }

        # Custo de movimento por tipo de terreno (paredes e pontos especiais têm custo 0)
        self.costs = {"#": 0, "G": 1, "L": 5, "I": 0, "F": 0}

        # Terrenos que podem aparecer aleatoriamente nas células do labirinto
        self.places = ["G", "L"]

        # Posição inicial: canto superior esquerdo [linha 0, coluna 0]
        self.initialPositions = [0, 0]

        # Posição final: canto inferior direito
        self.finalPosition = [self.size - 1, self.size - 1]

    def createMaze(self):
        # Preenche a grade com terrenos aleatórios (G ou L)
        self.matrix = np.random.choice(self.places, size=(self.size, self.size))

        # Define as paredes, início, fim e depois monta o grafo
        self.__defineWalls()
        self.__defineStartAndFinish()
        self.__defineGraph()

    def __defineStartAndFinish(self):
        # Marca a célula [0][0] como início (I) e a última célula como fim (F)
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
        # e as arestas conectam células vizinhas (cima, baixo, esquerda, direita)
        self.maze = nx.Graph()

        # Transforma a matriz 2D em uma lista linear para facilitar o acesso por índice
        self.matrixFlat = self.matrix.flatten()

        # Índice da última célula da primeira linha (limite superior para conexão vertical para cima)
        firstRow = len(self.matrix) - 1

        # Índice da primeira célula da última linha (limite inferior para conexão vertical para baixo)
        lastRow = len(self.matrix) * (len(self.matrix) - 1)

        # Índices das células na primeira coluna (não têm vizinho à esquerda)
        firstColumn = [
            index
            for index, num in enumerate(range(len(self.matrixFlat)))
            if index % self.size == 0
        ]

        # Índices das células na última coluna (não têm vizinho à direita)
        lastColumn = [
            index + (self.size - 1)
            for index, _ in enumerate(range(len(self.matrixFlat)))
            if index % self.size == 0
        ]

        # Percorre cada célula da matriz linearizada para criar nós e arestas no grafo
        for index, value in enumerate(self.matrixFlat):
            if self.__isWall(index):
                continue  # Pula paredes — elas não participam do grafo de caminhos

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
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index - self.size)

            # Tenta conectar com a célula de baixo (índice + size)
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
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index + self.size)

            # Tenta conectar com a célula à esquerda (índice - 1), se não estiver na primeira coluna
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
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index - 1)

            # Tenta conectar com a célula à direita (índice + 1), se não estiver na última coluna
            if index not in lastColumn:
                if not self.__isWall(index + 1):
                    self.maze.add_node(
                        index,
                        terrain=self.matrixFlat[index],
                        cost=self.matrixFlat[index],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_node(
                        index + 1,
                        terrain=self.matrixFlat[index + 1],
                        cost=self.matrixFlat[index + 1],
                        coordinates=self.__resolveCoordinates(index),
                    )
                    self.maze.add_edge(index, index + 1)

    def __positionExists(self, pos):
        # Verifica se uma posição está dentro dos limites da matriz
        return 0 <= pos <= self.matrix.shape[0]

    def __isWall(self, pos):
        # Atualmente retorna sempre False — ou seja, as paredes também entram no grafo.
        # Para excluir paredes do grafo, bastaria remover a linha abaixo e ativar a segunda.
        return False  # caso retorne falso monta grafo com as paredes também
        return self.matrixFlat[pos] == "#"

    def __resolveCoordinates(self, index):
        # Converte um índice linear de volta para coordenadas (linha, coluna) na grade
        row = 0
        column = 0
        for i in range(1, index):
            if i % self.size == 0:
                row += 1
                column = 0
            column += 1
        return (row, column)

    def getGraph(self):
        # Retorna o grafo montado do labirinto
        return self.maze

    def getMatrix(self):
        # Retorna a matriz 2D do labirinto
        return self.matrix

    def showMatrix(self):
        # Imprime a matriz do labirinto no terminal para visualização rápida
        print(self.matrix)
