from PyOptimizer import CForwardDiff
from PyOptimizer import CCentralDiff


def TestFun(x):
    return x[0]-x[1]+2*(x[0]**2)+2*x[0]*x[1]+x[1]**2

def DetermineDiff():
    Diff = CForwardDiff(TestFun, [0., 0.], 2)
    d = Diff.GetGrad(0)
    print(d)

if __name__ == "__main__":
    DetermineDiff()
