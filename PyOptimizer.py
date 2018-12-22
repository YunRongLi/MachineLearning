import math
from PyLineSearch import CFiSearch
from PyLineSearch import CGSSearch

class CForwardDiff():
    def __init__(self, costfunc, x, dim, eps=1e-5, percent=1e-5):
        self.__costfunc = costfunc
        self.__x = x
        self.__dim = dim
        self.__eps = eps
        self.__percent = percent

    @property
    def costfunc(self):
        return self.__costfunc

    @costfunc.setter
    def costfunc(self, costfunc):
        self.__costfunc = costfunc

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, value):
        self.__dim = value

    @property
    def eps(self):
        return self.__eps

    @eps.setter
    def eps(self, value):
        self.__eps = value

    @property
    def percent(self):
        return self.__percent

    @percent.setter
    def percent(self, value):
        self.__percent = value  

    def GetGrad(self, x):
        d = []
        fun = self.costfunc
        g = fun(x)
        for index in range(0, self.dim):
            x = self.x.copy()
            h = x[index] * self.percent + self.eps
            x[index] = x[index] + h
            d.append((fun(x)-g)/h)
        
        return d

class CBackwardDiff(CForwardDiff):
    def __init__(self, costfunc, x, dim, eps=1e-5, percent=1e-5):
        super(CBackwardDiff, self).__init__(costfunc, x, dim, eps, percent)

    def GetGrad(self, x):
        d = []
        fun = self.costfunc
        g = fun(x)
        for index in range(0, self.dim):
            x = self.x.copy()
            h = x[index] * self.percent + self.eps
            x[index] = x[index] - h
            d.append((g-fun(x))/h)

        return d

class CCentralDiff(CForwardDiff):
    def __init__(self, costfunc, x, dim, eps=1e-5, percent=1e-5):
        super(CCentralDiff, self).__init__(costfunc, x, dim, eps, percent)

    def GetGrad(self,x):
        d = []
        fun = self.costfunc
        for index in range(0, self.dim):
            x_forward = self.x.copy()
            x_backward = self.x.copy()
            h = x_forward[index] * self.percent + self.eps
            x_forward[index] = x_forward[index] + h/2
            x_backward[index] = x_backward[index] - h/2
            d.append((fun(x_forward)-fun(x_backward))/h)
        return d

class CGradDecent():
    def __init__(self, costfunc, x0, dim, Gradient='Backward', LineSearch='FiS', MinNorm=0.001, MaxIter=1000):
        self.__x0 = x0
        self.__dim = dim
        self.__MaxIter = MaxIter
        self.__MinNorm = MinNorm        
        self.__costfunc = costfunc
        self.__LineSearch = LineSearch
        self.__Gradient = Gradient

    @property
    def x0(self):
        return self.__x0

    @x0.setter
    def x0(self, value):
        self.__x0 = value

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, value):
        self.__dim = value

    @property
    def MaxIter(self):
        return self.__MaxIter

    @MaxIter.setter
    def MaxIter(self, value):
        self.__MaxIter = value

    @property
    def MinNorm(self):
        return self.__MinNorm

    @MinNorm.setter
    def MinNorm(self, value):
        self.__MinNorm = value

    @property
    def costfunc(self):
        return self.__costfunc

    @costfunc.setter
    def costfunc(self, value):
        self.__costfunc = value

    @property
    def LineSearch(self):
        return self.__LineSearch

    @LineSearch.setter
    def LineSearch(self, value):
        self.__LineSearch = value

    @property
    def Gradient(self):
        return self.__Gradient

    @Gradient.setter
    def Gradient(self, value):
        self.Gradient = value

    def RunOptimize(self):
        x = self.x0
        k = 0
        d = 1

        fun = self.costfunc

        if (self.LineSearch == "FiS"):
            LineSearch = CFiSearch(fun, x, d)
        else:
            LineSearch = CGSSearch(fun, x, d)

        if (self.Gradient == 'Forward'):
            Diff = CForwardDiff(fun, x, self.dim)
        elif (self.Gradient == 'Backward'):
            Diff = CBackwardDiff(fun, x, self.dim)
        else:
            Diff = CCentralDiff(fun, x, self.dim)

        grad_Magnitude = math.inf
        
        while (k < self.MaxIter):
            print('Optimizer Iter[', k, ']')

            if (k != 0):
                Diff.x = x 
              
            grad = Diff.GetGrad(x)

            grad_Magnitude = math.sqrt(math.fsum([i*i for i in grad]))
            print('||Gradient||: ',grad_Magnitude)
            if (grad_Magnitude < self.MinNorm):
                return x

            d = [-i for i in grad]
            
            if (k != 0):
                LineSearch.x = x
            
            LineSearch.d = d            

            alpha = LineSearch.RunSearch()

            x = [x[i] + alpha * d[i] for i in range(0, len(x))]
            print('X:', x)
            k += 1

        return x


        
        