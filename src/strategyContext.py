from src.strategies.aStarStrategy import AStarStrategy
from src.strategies.breadthStrategy import BreadthFirstSearchStrategy
from src.strategies.depthStrategy import DepthFirstSearchStrategy
from src.strategies.greedyStrategy import GreedyStrategy


class StrategyContext:
    """
    Implementa o padrão de projeto Strategy:
    recebe o nome do algoritmo escolhido pelo usuário e devolve a classe correspondente,
    sem que o código principal precise saber detalhes de cada algoritmo.
    """

    def __init__(self, strategy: str):
        self.strategy = strategy  # Nome do algoritmo escolhido (ex: "astar", "breadth")

        # Dicionário que mapeia o nome do algoritmo para sua classe
        self.strategies = {
            "astar": AStarStrategy,              # Busca A* (custo real + heurística)
            "greedy": GreedyStrategy,            # Busca gulosa (só heurística, sem custo real)
            "depth": DepthFirstSearchStrategy,   # Busca em profundidade (DFS)
            "breadth": BreadthFirstSearchStrategy,  # Busca em largura (BFS)
        }

    def get(self):
        # Retorna a classe do algoritmo correspondente ao nome informado.
        # Se nenhuma estratégia foi passada, retorna False (nenhum algoritmo selecionado).
        return self.strategies[self.strategy] if self.strategy is not None else False
