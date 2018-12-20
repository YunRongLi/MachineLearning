from PyOptimizer import CForwardDiff
#from PyOptimizer import CCentralDiff


def TestFun(x):
    return x[0]-x[1]+2*(x[0]**2)+2*x[0]*x[1]+x[1]**2

def DetermineDiff():
    #CCDiff = CCentralDiff(TestFun, [0, 0], 2)
    FWDiff = CForwardDiff(TestFun, [0, 0], 2)
    #cd = CCDiff.GetGrad(0)
    fd = FWDiff.GetGrad(0)

    #print('Central Gradient', cd)
    print('Forward Gradient', fd)

if __name__ == "__main__":
    DetermineDiff()
