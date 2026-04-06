import time


class TimerMetric:
    """
    Cronômetro simples para medir quanto tempo o algoritmo de busca levou
    para encontrar o caminho no labirinto.
    """

    def __init__(self):
        self.init = 0    # Momento em que o cronômetro foi iniciado
        self.result = 0  # Tempo total decorrido (em segundos)

    def start(self):
        # Registra o instante atual como ponto de partida da medição
        self.init = time.time()

    def stop(self):
        # Calcula a diferença entre agora e o momento de início
        self.result = time.time() - self.init

    def show(self):
        # Exibe o tempo de execução com 5 casas decimais
        print(f"Execution time is: {self.result:.5f} seconds")
