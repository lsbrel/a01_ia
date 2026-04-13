import argparse


class ArgumentParser:
    """
    Responsável por coletar as configurações da execução de forma interativa:
    pergunta ao usuário sobre tamanho do labirinto, paredes e algoritmo,
    validando cada entrada antes de prosseguir.
    """

    # Mapeamento de opções numéricas para os nomes internos das estratégias
    STRATEGY_OPTIONS = {
        "1": "breadth",
        "2": "depth",
        "3": "greedy",
        "4": "astar",
        "5": "all",
    }

    def bootstrap(self):
        # Coleta todas as configurações e retorna como objeto com atributos
        print("\n=== Configuração do Labirinto ===\n")

        size = self.__askSize()
        walls = self.__askWalls(size)
        visibleWalls = self.__askVisibleWalls()
        strategy = self.__askStrategy()

        # Retorna um Namespace para manter compatibilidade com o main.py
        return argparse.Namespace(
            size=size,
            walls=walls,
            visibleWalls=visibleWalls,
            strategy=strategy,
        )

    def __askSize(self):
        # Pergunta o tamanho do labirinto e valida que é um inteiro positivo
        while True:
            raw = input("Tamanho do labirinto (ex: 5 para uma grade 5x5): ").strip()
            if raw.isdigit() and int(raw) > 1:
                return int(raw)
            print("  Valor inválido. Informe um número inteiro maior que 1.\n")

    def __askWalls(self, size):
        # Pergunta a quantidade de paredes não pode exceder as células internas do labirinto
        maxWalls = (size * size) - 2  # desconta início e fim
        while True:
            raw = input(f"Quantidade de paredes (0 a {maxWalls}): ").strip()
            if raw.isdigit() and 0 <= int(raw) <= maxWalls:
                return int(raw)
            print(f"  Valor inválido. Informe um número entre 0 e {maxWalls}.\n")

    def __askVisibleWalls(self):
        # Pergunta se as paredes devem aparecer no grafo (s/n)
        while True:
            raw = input("Paredes visíveis no grafo? (s/n): ").strip().lower()
            if raw in ("s", "n"):
                return raw == "s"
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.\n")

    def __askStrategy(self):
        # Exibe as opções de algoritmo e aguarda uma escolha válida
        print("\n=== Algoritmo de Busca ===\n")
        print("  1. Busca em Largura  (breadth)")
        print("  2. Busca em Profundidade (depth)")
        print("  3. Busca Gulosa      (greedy)")
        print("  4. A*                (astar)")
        print("  5. Todos             (all)")

        while True:
            raw = input("\nEscolha uma opção (1-5): ").strip()
            if raw in self.STRATEGY_OPTIONS:
                return self.STRATEGY_OPTIONS[raw]
            print("  Opção inválida. Digite um número entre 1 e 5.\n")
