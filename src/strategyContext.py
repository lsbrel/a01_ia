from src.strategies.aStarStrategy import AStarStrategy
from src.strategies.breadthStrategy import BreadthFirstSearchStrategy
from src.strategies.depthStrategy import DepthFirstSearchStrategy
from src.strategies.greedyStrategy import GreedyStrategy


class StrategyContext:

    def __init__(self, strategy: str):
        self.strategy = strategy  # Nome do algoritmo escolhido

        # Dicionário que mapeia o nome do algoritmo para sua classe
        self.strategies = {
            "astar": AStarStrategy, # Busca A*
            "greedy": GreedyStrategy, # Busca gulosa
            "depth": DepthFirstSearchStrategy, # Busca em profundidade
            "breadth": BreadthFirstSearchStrategy, # Busca em largura
        }

    def get(self):
        # Retorna a classe do algoritmo correspondente ao nome informado.
        # Se nenhuma estratégia foi passada, retorna False (nenhum algoritmo selecionado).
        return self.strategies[self.strategy] if self.strategy is not None else False
