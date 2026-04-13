#!/bin/python3

# Importa as classes responsáveis por cada parte do sistema
from src.argumentParser import ArgumentParser  # Lê os argumentos da linha de comando
from src.strategyContext import StrategyContext  # Escolhe qual algoritmo de busca usar
from src.mazeBuilder import MazeBuilder  # Constrói o labirinto
from src.mazeResolutionAnimation import MazeResolutionAnimation  # Anima a resolução
from src.timerMetric import TimerMetric  # Mede o tempo de execução

# Lê os argumentos passados pelo usuário no terminal (--size, --walls, --strategy)
arguments = ArgumentParser().bootstrap()

# Cria o cronômetro que vai medir quanto tempo o algoritmo leva para resolver o labirinto
metrics = TimerMetric()

# Cria o labirinto com o tamanho e quantidade de paredes informados pelo usuário
maze = MazeBuilder(
    size=arguments.size, walls=arguments.walls, visibleWalls=arguments.visibleWalls
)
maze.createMaze()  # Gera a matriz do labirinto com terrenos, paredes, início e fim

maze.showMatrix()
maze.showLegend()  # Exibe a legenda dos tipos de terreno e seus custos

# Nomes legíveis para exibição na animação
STRATEGY_LABELS = {
    "breadth": "Busca em Largura",
    "depth":   "Busca em Profundidade",
    "greedy":  "Busca Gulosa",
    "astar":   "A*",
}

if arguments.strategy == "all":
    for strategy_key in ["breadth", "depth", "greedy", "astar"]:
        strategyContext = StrategyContext(strategy=strategy_key)
        strategy = strategyContext.get()(maze=maze)

        if strategy:
            print(f"\n{'─' * 50}")
            print(f"  {STRATEGY_LABELS[strategy_key]}")
            print(f"{'─' * 50}")

            metrics.start()
            strategy.run()
            metrics.stop()
            metrics.show()

            # Armazena expansão e caminho para passar à animação
            expansion = strategy.getExpansionOrder()
            path = strategy.getResolutionPath()

            animtation = MazeResolutionAnimation(
                maze=maze.getGraph(),
                expansion_order=expansion,
                path=path,
                strategy_name=STRATEGY_LABELS[strategy_key],
            )
            animtation.run()

else:
    strategyContext = StrategyContext(strategy=arguments.strategy)
    strategy = strategyContext.get()(maze=maze)

    if strategy:
        print(f"\n{'─' * 50}")
        print(f"  {STRATEGY_LABELS[arguments.strategy]}")
        print(f"{'─' * 50}")

        metrics.start()
        strategy.run()
        metrics.stop()
        metrics.show()

        # Armazena expansão e caminho para passar à animação
        expansion = strategy.getExpansionOrder()
        path = strategy.getResolutionPath()

        animtation = MazeResolutionAnimation(
            maze=maze.getGraph(),
            expansion_order=expansion,
            path=path,
            strategy_name=STRATEGY_LABELS[arguments.strategy],
        )
        animtation.run()
