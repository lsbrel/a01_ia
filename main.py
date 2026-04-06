#!/bin/python3

# Importa as classes responsáveis por cada parte do sistema
from src.argumentParser import ArgumentParser        # Lê os argumentos da linha de comando
from src.strategyContext import StrategyContext      # Escolhe qual algoritmo de busca usar
from src.mazeBuilder import MazeBuilder              # Constrói o labirinto
from src.mazeResolutionAnimation import MazeResolutionAnimation  # Anima a resolução
from src.timerMetric import TimerMetric              # Mede o tempo de execução

# Lê os argumentos passados pelo usuário no terminal (--size, --walls, --strategy)
arguments = ArgumentParser().bootstrap()

# Cria o cronômetro que vai medir quanto tempo o algoritmo leva para resolver o labirinto
metrics = TimerMetric()

# Cria o labirinto com o tamanho e quantidade de paredes informados pelo usuário
maze = MazeBuilder(size=arguments.size, walls=arguments.walls)
maze.createMaze()  # Gera a matriz do labirinto com terrenos, paredes, início e fim

# Seleciona o algoritmo de busca escolhido pelo usuário (ex: breadth, depth, astar, greedy)
strategyContext = StrategyContext(strategy=arguments.strategy)
strategy = strategyContext.get()(maze=maze)  # Instancia o algoritmo com o labirinto

if arguments.strategy == "all":
    for strategy in ["breadth", "depth", "greedy", "astar"]:
        strategyContext = StrategyContext(strategy=strategy)
        strategy = strategyContext.get()(maze=maze)

        if strategy:
            metrics.start()

            strategy.run()
            print(strategy.getResolutionPath())

            metrics.stop()
            metrics.show()

            animtation = MazeResolutionAnimation(
                maze=maze.getGraph(), path=strategy.getResolutionPath()
            )
            animtation.run()

else:
    strategyContext = StrategyContext(strategy=arguments.strategy)
    strategy = strategyContext.get()(maze=maze)

    if strategy:
        metrics.start()
        strategy.run()

        metrics.stop()
        metrics.show()

        animtation = MazeResolutionAnimation(
            maze=maze.getGraph(), path=strategy.getResolutionPath()
        )
        animtation.run()
