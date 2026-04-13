import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation


class MazeResolutionAnimation:

    def __init__(self, maze, expansion_order, path, strategy_name=""):
        # Grafo do labirinto
        self.maze = maze                      
        # Ordem de expansão dos nós durante a busca  
        self.expansion_order = expansion_order
        # Caminho final do início ao fim
        self.path = path
        # Nome legível do algoritmo em uso
        self.strategy_name = strategy_name

        # Mapeamento de tipos de terreno para cores na visualização
        self.terrains = {
            # Parede
            "#": "gray",
            # Grama      
            "G": "green",
            # Calçada    
            "C": "lightgray",
            # Lama   
            "L": "brown",
            # Início
            "I": "tab:blue",
            # Fim
            "F": "tab:blue",
        }

        # Define a cor de cada nó com base no terreno
        self.colors = [
            self.terrains[node[1]["terrain"]] for node in self.maze.nodes(data=True)
        ]

        # Figura maior para acomodar legenda sem sobrepor o grafo
        self.fig, self.ax = plt.subplots(figsize=(10, 8))

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

        # Titulo
        self.fig.suptitle(f"Algoritmo: {self.strategy_name}", fontsize=13, fontweight="bold")

        # Exibe legenda e título iniciais antes da animação começar
        self.__drawLegend()
        self.ax.set_title("Aguardando início da animação...", fontsize=10, pad=8)

        # Total de frames = expansão + caminho final
        total_frames = len(self.expansion_order) + len(self.path)

        # Cria a animação com os dois grupos de frames em sequência
        self.anim = animation.FuncAnimation(
            self.fig,
            self.__animate,
            frames=total_frames,
            interval=500, # Intervalo de cada animação
            init_func=self.__initAnimation,
            repeat=False, # Não repete a animação ao terminar
        )

        # Abre a janela da animação
        plt.show()

    def __initAnimation(self):
        # Função de inicialização da animação
        pass

    def __animate(self, frame):
        self.ax.clear()  # Limpa o desenho anterior

        if frame < len(self.expansion_order):
            # Fase 1: pinta o nó explorado de laranja (ordem de expansão do algoritmo)
            node_id = self.expansion_order[frame]
            normalizedIndex = list(self.maze.nodes).index(node_id)
            self.colors[normalizedIndex] = "orange"

            # Título indica a fase atual e o progresso
            step = frame + 1
            total = len(self.expansion_order)
            self.ax.set_title(
                f"Fase 1: Explorando nós | Passo {step} de {total} | Nó atual: {node_id}",
                fontsize=10, pad=8
            )
        else:
            # Fase 2: pinta o nó do caminho final de vermelho (solução encontrada)
            path_frame = frame - len(self.expansion_order)
            node_id = self.path[path_frame]
            normalizedIndex = list(self.maze.nodes).index(node_id)
            self.colors[normalizedIndex] = "red"

            # Título indica caminho final
            step = path_frame + 1
            total = len(self.path)
            self.ax.set_title(
                f"Fase 2: Caminho final | Passo {step} de {total} | Nó atual: {node_id}",
                fontsize=10, pad=8
            )

        # Redesenha o grafo com as cores atualizadas
        nx.draw(
            self.maze,
            pos=self.layout,
            ax=self.ax,
            with_labels=True,
            node_color=self.colors,
        )

        # Redesenha a legenda
        self.__drawLegend()

    def __drawLegend(self):
        # Constrói a legenda com patches coloridos para cada tipo de terreno e fase
        legend_entries = [
            mpatches.Patch(color="tab:blue",  label="Início / Fim"),
            mpatches.Patch(color="green",     label="Grama       (custo 1)"),
            mpatches.Patch(color="lightgray", label="Calçada     (custo 4)"),
            mpatches.Patch(color="brown",     label="Lama        (custo 5)"),
            mpatches.Patch(color="gray",      label="Parede      (intransponível)"),
            mpatches.Patch(color="orange",    label="Nó explorado (fase 1)"),
            mpatches.Patch(color="red",       label="Caminho final (fase 2)"),
        ]

        # Posiciona a legenda fora da área do grafo
        self.ax.legend(
            handles=legend_entries,
            loc="lower right",
            fontsize=8,
            framealpha=0.9,
        )
