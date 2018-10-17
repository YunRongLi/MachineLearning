import numpy as np
import matplotlib.pyplot as plt

from PyLineSearch import PyLineSearch

def func(x):
    return x**4 - 14 * x**3 + 60 * x**2 - 70 * x

def DetermineMin():
    func1 = func
    Searcher = PyLineSearch()
    finalrange = 0.3
    X_min_golden = Searcher.Golden(func1, finalrange)
    X_min_fib = Searcher.Fibonacci(func1, finalrange, 0.1)
    Phase1 = Searcher.GetPhase1Interval()

    t1 = np.arange(Phase1[0], Phase1[1], finalrange/10)
    plt.figure(1)
    plt.plot(t1, func1(t1), 'k', X_min_golden, func1(X_min_golden), 'bo', X_min_fib, func1(X_min_fib), 'ro')
    plt.show()

if __name__ == "__main__":
    DetermineMin()
    
    