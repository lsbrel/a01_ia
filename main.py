#!/bin/python3
from src.argumentParser import ArgumentParser
from src.strategyContext import StrategyContext
from src.mazeBuilder import MazeBuilder
from src.mazeResolutionAnimation import MazeResolutionAnimation
from src.timerMetric import TimerMetric

arguments = ArgumentParser().bootstrap()
metrics = TimerMetric()

maze = MazeBuilder(size=arguments.size, walls=arguments.walls)
maze.createMaze()

strategyContext = StrategyContext(strategy=arguments.strategy)
strategy = strategyContext.get()(maze=maze)

if strategy:

    metrics.start()

    maze.showMatrix()
    strategy.run()
    print(strategy.getResolutionPath())

    metrics.stop()
    metrics.show()

    animtation = MazeResolutionAnimation(
        maze=maze.getGraph(), path=strategy.getResolutionPath()
    )
    animtation.run()
