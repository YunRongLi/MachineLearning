import numpy as np
import matplotlib.pyplot as plt
import time

from PyLineSearch import CGSSearch
from PyLineSearch import CFiSearch

def TestLineFun1(x):
    return x**4 - 14 * x**3 + 60 * x**2 - 70 * x

def TestLineFun2(x):
    return (0.65-0.75/(1+x**2))-0.65*x*np.arctan2(1,x)

def TestLineFun3(x):
    return -(108*x-x**3)/4

def Test2VarFun3(x):
    return -x[0]*x[1]*np.exp(-x[0]**-x[1]**2)
    # x* = [0.7071, 0.7071] or x* = [-0.7071, -0.7071], f(x*) = -0.1839

def DetermineMin():
    func1 = Test2VarFun3
    #func2 = TestLineFun2
    #func3 = TestLineFun3
    
    Searcher = CGSSearch(func1,[0, 0], 0.1, 0.01)
    #finalrange = 0.3
    tStart = time.time()
    X = Searcher.RunSearch()
    tEnd = time.time()

    print("Time cost:  %f sec" %(tEnd - tStart))
    #X_min_fib = Searcher.Fibonacci(func1, finalrange, 0.1)
    #Phase1 = Searcher.GetPhase1Interval()

    f_X = func1(X)
    print('X: ', X, ' f(X): ', f_X)

    # plt.figure(1)
    # plt.xlabel('x')
    # plt.ylabel('f(x)')
    # plt.plot(t1, func1(t1), 'k', X_min_golden, func1(X_min_golden))
    # plt.legend(('f(x)', 'Golden', 'Fibonacci'), loc='lower right', shadow=True)
    # plt.grid(True)

    # X_min_golden = Searcher.Golden(func2, finalrange)
    # X_min_fib = Searcher.Fibonacci(func2, finalrange, 0.1)
    # Phase1 = Searcher.GetPhase1Interval()
    # t1 = np.arange(Phase1[0], Phase1[1], finalrange/10)
    
    # plt.figure(2)
    # plt.xlabel('x')
    # plt.ylabel('f(x)')
    # plt.plot(t1, func1(t1), 'k', X_min_golden, func1(X_min_golden), 'bo', X_min_fib, func1(X_min_fib), 'ro')
    # plt.legend(('f(x)', 'Golden', 'Fibonacci'), loc='upper right', shadow=True)
    # plt.grid(True)

    plt.show()

if __name__ == "__main__":
    DetermineMin()
    
    