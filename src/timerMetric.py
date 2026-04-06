import time


class TimerMetric:

    def __init__(self):
        self.init = 0
        self.result = 0

    def start(self):
        self.init = time.time()

    def stop(self):
        self.result = time.time() - self.init

    def show(self):
        print(f"Execution time is: {self.result:.5f} seconds")
