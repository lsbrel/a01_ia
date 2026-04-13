import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation


class MazeResolutionAnimation:
    """
    Gera uma animação gráfica em duas fases:
      Fase 1 — laranja: mostra a ordem em que o algoritmo expandiu os nós
      Fase 2 — vermelho: destaca o caminho final encontrado do início ao fim
    """

    def __init__(self, maze, expansion_order, path):
        self.maze = maze                        # Grafo do labirinto
        self.expansion_order = expansion_order  # Ordem de expansão dos nós durante a busca
        self.path = path                        # Caminho final do início ao fim

        # Mapeamento de tipos de terreno para cores na visualização
        self.terrains = {
            "#": "gray",        # Parede
            "G": "green",       # Grama
            "C": "lightgray",   # Calçada
            "L": "brown",       # Lama
            "I": "tab:blue",    # Início
            "F": "tab:blue",    # Fim
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

        # Total de frames = expansão + caminho final
        total_frames = len(self.expansion_order) + len(self.path)

        # Cria a animação com os dois grupos de frames em sequência
        self.anim = animation.FuncAnimation(
            self.fig,
            self.__animate,
            frames=total_frames,
            interval=500,           # 500ms entre cada frame
            init_func=self.__initAnimation,
            repeat=False,           # Não repete a animação ao terminar
        )

        # Abre a janela gráfica com a animação
        plt.show()

    def __initAnimation(self):
        # Função de inicialização da animação (vazia — estado inicial já foi desenhado em run())
        pass

    def __animate(self, frame):
        self.ax.clear()  # Limpa o desenho anterior

        if frame < len(self.expansion_order):
            # Fase 1: pinta o nó explorado de laranja (ordem de expansão do algoritmo)
            node_id = self.expansion_order[frame]
            normalizedIndex = list(self.maze.nodes).index(node_id)
            self.colors[normalizedIndex] = "orange"
        else:
            # Fase 2: pinta o nó do caminho final de vermelho (solução encontrada)
            path_frame = frame - len(self.expansion_order)
            node_id = self.path[path_frame]
            normalizedIndex = list(self.maze.nodes).index(node_id)
            self.colors[normalizedIndex] = "red"

        # Redesenha o grafo com as cores atualizadas
        nx.draw(
            self.maze,
            pos=self.layout,
            ax=self.ax,
            with_labels=True,
            node_color=self.colors,
        )
