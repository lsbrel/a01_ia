import argparse


class ArgumentParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def bootstrap(self):
        self.defineArguments()
        return self.parser.parse_args()

    def defineArguments(self):
        self.parser.add_argument("--size", type=int)
        self.parser.add_argument("--walls", type=int)
        self.parser.add_argument(
            "--strategy", choices=["breadth", "depth", "astar", "greedy"]
        )
