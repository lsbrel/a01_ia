import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation


class MazeResolutionAnimation:
    """
    Gera uma animação gráfica mostrando o labirinto como grafo
    e destaca, frame a frame, os nós visitados pelo algoritmo de busca.
    """

    def __init__(self, maze, path):
        self.maze = maze  # Grafo do labirinto (nós = células, arestas = conexões)
        self.path = path  # Lista de nós visitados pelo algoritmo, na ordem de visita

        # Mapeamento de tipos de terreno para cores na visualização
        self.terrains = {
            "#": "gray",       # Parede
            "G": "green",      # Grama
            "L": "brown",      # Lama
            "I": "tab:blue",   # Início
            "F": "tab:blue",   # Fim
        }

        # Define a cor inicial de cada nó com base no tipo de terreno armazenado no grafo
        self.colors = [
            self.terrains[node[1]["terrain"]] for node in self.maze.nodes(data=True)
        ]

        # Cria a figura e os eixos do matplotlib para renderizar o grafo
        self.fig, self.ax = plt.subplots()

        # Define o posicionamento dos nós na tela usando BFS a partir do nó 0
        self.layout = nx.bfs_layout(self.maze, start=0)

    def run(self):
        # Desenha o estado inicial do grafo com as cores de cada terreno
        nx.draw(
            self.maze,
            pos=self.layout,
            ax=self.ax,
            with_labels=True,
            node_color=self.colors,
        )

        # Cria a animação: a cada frame (1 por segundo), chama __animate
        # para colorir o próximo nó do caminho percorrido
        self.anim = animation.FuncAnimation(
            self.fig,
            self.__animate,
            frames=len(self.path),  # Total de frames = total de nós visitados
            interval=1000,          # 1000ms = 1 segundo entre cada frame
            init_func=self.__initAnimation,
            repeat=False,           # Não repete a animação ao terminar
        )

        # Abre a janela gráfica com a animação
        plt.show()

    def __initAnimation(self):
        # Função de inicialização da animação (vazia — estado inicial já foi desenhado em run())
        pass

    def __animate(self, frame):
        # Chamada a cada frame da animação
        if frame < len(self.path):
            self.ax.clear()  # Limpa o desenho anterior

            # Encontra a posição do nó atual na lista de nós do grafo
            normalizedIndex = list(self.maze.nodes).index(self.path[frame])

            # Pinta o nó atual de laranja para indicar que foi visitado neste passo
            self.colors[normalizedIndex] = "orange"

            # Redesenha o grafo com as cores atualizadas
            nx.draw(
                self.maze,
                pos=self.layout,
                ax=self.ax,
                with_labels=True,
                node_color=self.colors,
            )
