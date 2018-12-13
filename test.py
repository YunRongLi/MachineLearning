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

def Test2VarFun1(x):
    return (x[0]-x[1]+2*(x[0]**2)+2*x[0]*x[1]+x[1]**2)

def Test2VarFun3(x):
    return -x[0]*x[1]*np.exp(-x[0]**2-x[1]**2)

def DetermineMin():
    func1 = Test2VarFun1
    CGSSearcher = CGSSearch(func1, [0, 0], 0.1, 0.1)
    #CFiSearcher = CFiSearch(func1, 0, 0.1, 0.1)
    #finalrange = 0.3
    x_ = CGSSearcher.RunSearch()

    #gsX = CGSSearcher.RunSearch()
    #fiX = CFiSearcher.RunSearch()
    #gsf_X = func1(gsX)
    #fif_x = func1(fiX)
    #print('GS X: ',  gsX, 'GS F(X): ', gsf_X)
    #print('Fi X: ', fiX, 'Fi F(X): ', fif_x)
    # t1 = np.arange(1, 8, 0.01)
    # plt.figure(1)
    # plt.xlabel('x')
    # plt.ylabel('f(x)')
    # plt.plot(t1, func1(t1), 'k', gsX, gsf_X, 'bo', fiX, fif_x, 'ro')
    # plt.legend(('f(x)', 'Golden', 'Fibonacci'), loc='lower right', shadow=True)
    # plt.grid(True)
    # plt.show()

if __name__ == "__main__":
    DetermineMin()
    
    