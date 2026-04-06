import argparse


class ArgumentParser:
    """
    Responsável por ler e interpretar os argumentos passados pelo usuário
    na linha de comando, como o tamanho do labirinto e o algoritmo a usar.
    """

    def __init__(self):
        # Cria o objeto que vai processar os argumentos do terminal
        self.parser = argparse.ArgumentParser()

    def bootstrap(self):
        # Define quais argumentos são aceitos e retorna os valores já interpretados
        self.defineArguments()
        return self.parser.parse_args()

    def defineArguments(self):
        # --size: tamanho do labirinto (ex: 5 gera uma grade 5x5)
        self.parser.add_argument("--size", type=int)

        # --walls: quantidade de paredes aleatórias a inserir no labirinto
        self.parser.add_argument("--walls", type=int)

        # --strategy: qual algoritmo de busca usar para resolver o labirinto
        # Opções disponíveis: busca em largura, profundidade, A* e guloso
        self.parser.add_argument(
            "--strategy", choices=["breadth", "depth", "astar", "greedy", "all"]
        )
