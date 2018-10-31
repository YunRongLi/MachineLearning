import numpy as np
import matplotlib.pyplot as plt

from PyLineSearch import PyLineSearch

def TestLineFun1(x):
    return x**4 - 14 * x**3 + 60 * x**2 - 70 * x

def TestLineFun2(x):
    return (0.65-0.75/(1+x**2))-0.65*x*np.arctan2(1,x)

def TestLineFun3(x):
    return -(108*x-x**3)/4

def DetermineMin():
    func1 = TestLineFun3
    Searcher = PyLineSearch()
    finalrange = 0.3
    X_min_golden = Searcher.Golden(func1, finalrange)
    X_min_fib = Searcher.Fibonacci(func1, finalrange, 0.1)
    Phase1 = Searcher.GetPhase1Interval()

    

    t1 = np.arange(Phase1[0], Phase1[1], finalrange/10)
    plt.figure(1)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.plot(t1, func1(t1), 'k', X_min_golden, func1(X_min_golden), 'bo', X_min_fib, func1(X_min_fib), 'ro')
    plt.legend(('f(x)', 'Golden', 'Fibonacci'), loc='lower right', shadow=True)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    DetermineMin()
    
    