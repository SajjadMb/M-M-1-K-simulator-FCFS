import math
import numpy as np
from typing import Tuple


class Analyze:
    def __init__(self, mu, teta, lam, queue_size=12, is_expnential=True) -> None:
        self.mu: float = mu
        self.teta: float = teta
        self.lam: int = lam
        self.queue_size: int = queue_size
        self.is_expnential = is_expnential
        self.PB = 0
        self.PD = 0

    def CalculatePhi(self, n):
        return self.exponentialPhi(n) if self.is_expnential else self.constantPhi(n)

    def exponentialPhi(self, n):
        return math.factorial(n) / math.prod([(self.mu + i/self.teta) for i in range(n + 1)])

    def constantPhi(self, n):
        return math.factorial(n)/(self.mu ** (n+1)) * (1 - (math.e**(-1 * self.mu * self.teta)) * sum([((self.mu * self.teta) ** i)/math.factorial(i) for i in range(n)]))

    def calculateX(self, n):
        if n == 1:
            return self.lam/self.mu
        else:
            return ((self.lam ** n) * self.CalculatePhi(n-1)) / math.factorial(n-1)

    def calculatePB(self):
        self.PB = self.calculateP0() * self.calculateX(self.queue_size)
        return self.PB

    def calculateP0(self):
        return 1 / sum([self.calculateX(i) for i in range(1, 13)] + [1])

    def calculatePD(self):
        self.PD = (1 - (self.mu/self.lam) * (1 - self.calculateP0())) - self.PB
        return self.PD

    def analyze(self) -> Tuple[float, float]:
        self.calculatePB()
        self.calculatePD()
        return self.PB, self.PD
