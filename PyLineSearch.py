import numpy as np
from enum import Enum

class BoundaryChange(Enum):
    Nochange = 0
    Upper = 1
    Lower = 2
    Both = 3

class CGSSearch(object):
    def __init__(self, costfunc, x=0, delta=0.1, eps=0.01):
        self.__FibCoe = 1.618
        self.__x = x
        self.__delta = delta
        self.__eps = eps
        self.__costfunc = costfunc

    @property
    def FibCoe(self):
        return self.__FibCoe

    @FibCoe.setter
    def FibCoe(self, value):
        self.__FibCoe = value

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
    def x(self, x):
        self.__x = x    

    @property
    def delta(self):
        return self.__delta

    @delta.setter
    def delta(self, delta):
        self.__delta = delta

    @property
    def eps(self):
        return self.__eps

    @eps.setter
    def eps(self, eps):
        self.__eps = eps

    def Step(self, N):
        Step = 0
        for index in range(0, N+1):
            Step = Step + self.__delta * self.FibCoe**index
        return Step

    def Phase1(self):
        func = self.costfunc
        g_2 = 0
        g_1 = 0
        g   = 0        
        fg_2 = 0
        fg_1 = 0
        fg   = 0
        
        fg_2 = func(g_2)
        g_1 = self.__delta
        fg_1 = func(g_1)

        if (fg_1 >= fg_2):
            print('---Uncertainty Interval---')
            print('Lower: '+ g_2, ' ,Upper: ', g_1)
            return np.array([[g_2, np.nan, g_1], [fg_2, np.nan, fg_1]])

        index = 2
        #print('------------Phase 1 Start------------')
        while(True):
            if (index == 2):
                g = self.Step(index)
                fg   = func(g)
            else:
                g_2 = g_1
                g_1 = g
                g   = self.Step(index)

                fg_2 = fg_1
                fg_1 = fg
                fg   = func(g)
                
            if (fg_2 > fg_1 and fg_1 < fg):
                return np.array([[g_2, g_1, g], [fg_2, fg_1, fg]])

            index = index + 1

    def Phase2(self, phase1):
        func = self.costfunc
        rho = 0.382
        I_Lower = phase1[0, 0]
        I_Upper = phase1[0, 2]
        Interval = I_Upper - I_Lower
        if (Interval < self.__eps):
            return (I_Upper + I_Lower)/2

        MaxIter = 0
        while(True):
            if ((0.61893**MaxIter) <= (self.__eps/Interval)):
                break
            MaxIter += 1

        print('Max Iter: ', MaxIter)

        alpha = 0
        beta = 0
        f_alpha = 0
        f_beta = 0
        bound = BoundaryChange.Nochange

        for index in range(0, MaxIter):
            if (index == 0):
                if (phase1[0, 1] != np.nan):
                    alpha = phase1[0, 1]
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = phase1[1, 1]
                    f_beta = func(beta)

                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                    f_beta = func(beta)

            else:
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = I_Lower + (1 - rho) * Interval
                    f_beta = func(beta)
                elif (bound == BoundaryChange.Upper):
                    beta = alpha 
                    f_beta = f_alpha
                    alpha = I_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                    f_beta = func(beta)
            
            if (f_alpha < f_beta):
                I_Upper = beta
                bound = BoundaryChange.Upper
            elif (f_alpha > f_beta):
                I_Lower = alpha
                bound = BoundaryChange.Lower
            else:
                I_Lower = alpha
                I_Upper = beta
                bound = BoundaryChange.Both
            
            Interval = I_Upper - I_Lower

        return (I_Upper + I_Lower)/2

    def RunSearch(self):
        Phase1 = self.Phase1()
        print('CGSSearch Phase 1 Upper: ', Phase1[0, 0], 'Lower: ', Phase1[0,2])
        X = self.Phase2(Phase1)
        return X

class CFiSearch(CGSSearch):
    def __init__(self, costfunc, x=0, delta=0.1, eps=0.01):
        super(CFiSearch, self).__init__(costfunc, x, delta, eps)

    def FibSequence(self,n):
        if n < 2:
            return 1
        else:
            return self.FibSequence(n-1) + self.FibSequence(n-2)

    def Phase2(self, phase1):
        print('CFiSearcch Phase 2 Start')
        func = self.costfunc
        I_Lower = phase1[0, 0]
        I_Upper = phase1[0, 2]
        Interval = I_Upper - I_Lower
        eps = self.eps
        if (Interval < eps):
            return (I_Upper + I_Lower)/2

        MaxIter = 0
        while(True):
            if ((0.61893**MaxIter) <= (eps/Interval)):
                break
            MaxIter += 1
        print('Max Iter: ', MaxIter)

        alpha = 0
        beta = 0
        f_alpha = 0
        f_beta = 0
        bound = BoundaryChange.Nochange

        for index in range(0, MaxIter):
            if (index == 0):
                rho = 1 - (self.FibSequence(MaxIter)/ self.FibSequence(MaxIter+1))
                alpha = I_Lower + rho * Interval
                beta = I_Lower + (1 - rho) * Interval
                f_alpha = func(alpha)
                f_beta = func(beta)

            elif (index == (MaxIter-1)):
                rho = 0.5 - self.eps
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = I_Lower + (1 - rho) * Interval
                    f_beta = func(beta)

                elif (bound == BoundaryChange.Upper):
                    beta = alpha 
                    f_beta = f_alpha
                    alpha = I_Lower + rho * Interval
                    f_alpha = func(alpha)

                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                    f_beta = func(beta)

            else:
                rho = 1 - (self.FibSequence(MaxIter-index)/ self.FibSequence(MaxIter-index+1))
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = I_Lower + (1 - rho) * Interval
                    f_beta = func(beta)

                elif (bound == BoundaryChange.Upper):
                    beta = alpha 
                    f_beta = f_alpha
                    alpha = I_Lower + rho * Interval
                    f_alpha = func(alpha)

                else:
                    alpha = I_Lower + rho * Interval
                    beta = I_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                    f_beta = func(beta)

            if (f_alpha < f_beta):
                I_Upper = beta
                bound = BoundaryChange.Upper
            elif (f_alpha > f_beta):
                I_Lower = alpha
                bound = BoundaryChange.Lower
            else:
                I_Lower = alpha
                I_Upper = beta
                bound = BoundaryChange.Both

            Interval = I_Upper - I_Lower

        return (I_Lower + I_Upper) / 2

    def RunSearch(self):
        Phase1 = self.Phase1()
        print('CFiSearch Phase 1 Upper: ', Phase1[0, 0], 'Lower: ', Phase1[0, 2])
        X = self.Phase2(Phase1)
        return X
