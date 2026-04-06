from src.strategies.aStarStrategy import AStarStrategy
from src.strategies.breadthStrategy import BreadthFirstSearchStrategy
from src.strategies.depthStrategy import DepthFirstSearchStrategy
from src.strategies.greedyStrategy import GreedyStrategy


class StrategyContext:

    def __init__(self, strategy: str):
        self.strategy = strategy
        self.strategies = {
            "astar": AStarStrategy,
            "greedy": GreedyStrategy,
            "depth": DepthFirstSearchStrategy,
            "breadth": BreadthFirstSearchStrategy,
        }

    def get(self):
        return self.strategies[self.strategy] if self.strategy is not None else False
