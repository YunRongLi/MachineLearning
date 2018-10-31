import numpy as np
from enum import Enum

class BoundaryChange(Enum):
    Nochange = 0
    Upper = 1
    Lower = 2
    Both = 3

def FibSequence(n):
    if n < 2:
        return 1
    else:
        return FibSequence(n-1) + FibSequence(n-2)

class CGSSearch:
    def __init__(self, costfunc, x=0, delta=0.1, eps=0.01):
        self.__FibCoe = 1.618
        self.__x = x
        self.__delta = delta
        self.__eps = eps
        self.__costfunc = costfunc

    def set_costfunc(self, costfunc):
        self.__costfunc = costfunc

    def set_x(self, x):
        self.__x = x

    def set_delta(self, delta):
        self.__delta = delta

    def set_eps(self, eps):
        self.__eps = eps

    def __Step(self, N):
        Step = 0
        for index in range(0, N+1):
            Step = Step + self.__delta * self.__FibCoe**index
        return Step

    def Phase1(self):
        g_2 = 0
        g_1 = 0
        g   = 0        
        fg_2 = 0
        fg_1 = 0
        fg   = 0
        
        fg_2 = self.__costfunc(g_2)
        g_1 = self.__delta
        fg_1 = self.__costfunc(g_1)

        if (fg_1 >= fg_2):
            print('---Uncertainty Interval---')
            print('Lower: '+ g_2, ' ,Upper: ', g_1)
            return g_2, g_1, fg_2, fg_1

        index = 2
        #print('------------Phase 1 Start------------')
        while(True):
            if (index == 2):
                g = self.__Step(index)
                fg   = self.__costfunc(g)

            else:
                g_2 = g_1
                g_1 = g
                g   = self.__Step(index)

                fg_2 = fg_1
                fg_1 = fg
                fg   = self.__costfunc(g)

            if (fg_2 > fg_1 and fg_1 < fg):
                return g_2, g, fg_2, fg

            index = index + 1

    # def Phase2(self):

    def RunSearch(self):
        I_Lower, I_Upper = self.Phase1(*self.__delta)
        Interval = I_Upper - I_Lower

        if (Interval < self.__eps):
            x = (I_Upper + I_Lower)/2
            return x

        MaxIter = 0
        while(True):
            if ((0.61893**MaxIter) <= (self.__eps/Interval)):
                break
            MaxIter = MaxIter + 1

        







class PyLineSearch:
    def __init__(self, delta=0.1):
        self.__FibCoe = 1.618
        self.__rho    = 0.382
        self.__delta = delta
        self.__phase1Interval = [0, 0]

    def __Step(self, N):
        Step = 0
        for index in range(0, N+1):
            Step = Step + self.__delta * self.__FibCoe**index
        return Step

    def Golden(self, func, FinalRange):
        fg_2 = 0
        fg_1 = 0
        fg   = 0
        g_2 = 0
        g_1 = 0
        g   = 0

        Interval_Upper = 0
        Interval_Lower = 0

        #Phase 1 Find Interval of Interest
        index = 2
        print('------------Phase 1 Start------------')
        while(True):
            if (index == 2):
                g_2 = self.__Step(0)
                g_1 = self.__Step(index-1)
                g   = self.__Step(index)

                fg_2 = func(0)
                fg_1 = func(g_1)
                fg   = func(g)

                if (fg_2 > fg_1 and fg_1 < fg):
                    Interval_Lower = 0
                    Interval_Upper = g
                    break
            else:
                g_2 = self.__Step(index-2)
                g_1 = self.__Step(index-1)
                g   = self.__Step(index)

                fg_2 = func(g_2)
                fg_1 = func(g_1)
                fg   = func(g)

                if (fg_2 > fg_1 and fg_1 < fg):
                    Interval_Lower = g_2
                    Interval_Upper = g
                    break

            index = index + 1

        self.__phase1Interval[0] = Interval_Lower
        self.__phase1Interval[1] = Interval_Upper

        print('Uncertainty Interval Lower: ', Interval_Lower , ' Upper: ', Interval_Upper)
        print('------------Phase 1 Done-------------')

        #Phase 2 
        print('------------Phase 2 Start------------')
        Interval = Interval_Upper - Interval_Lower
        if (Interval < FinalRange):
            x = (Interval_Upper + Interval_Lower)/2
            return x

        Iteration_N = 0
        while(True):
            if ((0.61803**Iteration_N) <= (FinalRange/Interval)):
                break
            Iteration_N = Iteration_N + 1

        print('------Start Iterate----- Steps: ', Iteration_N)

        alpha = 0
        beta = 0
        f_alpha = 0
        f_beta = 0
        bound = BoundaryChange.Nochange

        for index in range(0, Iteration_N):
            print('Step:',index)
            if (index == 0):
                alpha = g_1
                beta = Interval_Lower + (1 - self.__rho) * Interval
                f_alpha = fg_1
                f_beta = func(beta)
                if (f_alpha < f_beta):
                    Interval_Upper = beta
                    bound = BoundaryChange.Upper
                    print('Upper Changed, Upper: ', Interval_Upper)
                elif (f_alpha > f_beta):
                    Interval_Lower = g_1
                    bound = BoundaryChange.Lower
                    print('Lower Changed, Lower: ', Interval_Lower)
                else:
                    Interval_Lower = g_1
                    Interval_Upper = beta
                    bound = BoundaryChange.Both
                    print('Both Changed, Lower: ', Interval_Lower, ' ,Upper: ', Interval_Upper)
                
                Interval = Interval_Upper - Interval_Lower
            else:
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = Interval_Lower + (1 - self.__rho) * Interval
                    f_beta = func(beta)

                elif(bound == BoundaryChange.Upper):
                    beta = alpha
                    f_beta = f_alpha
                    alpha = Interval_Lower + self.__rho * Interval
                    f_alpha = func(alpha)

                else:
                    alpha = Interval_Lower + self.__rho * Interval
                    beta  = Interval_Lower + (1 - self.__rho) * Interval
                    f_alpha = func(alpha)
                    f_beta  = func(beta)

                if (f_alpha < f_beta):
                    Interval_Upper = beta
                    bound = BoundaryChange.Upper
                    print('Upper Changed, Upper: ', Interval_Upper)
                elif(f_alpha > f_beta):
                    Interval_Lower = alpha
                    bound = BoundaryChange.Lower
                    print('Lower Changed, Lower: ', Interval_Lower)
                else:
                    Interval_Lower = alpha
                    Interval_Upper = beta
                    bound = BoundaryChange.Both
                    print('Both Changed, Lower: ', Interval_Lower, ' ,Upper: ', Interval_Upper)

                Interval = Interval_Upper - Interval_Lower

        print('Uncertainty Interval Lower: ', Interval_Lower , ' Upper: ', Interval_Upper)
        print('Interval: ', Interval)
        print('------------Phase 2 Done------------')

        x = (Interval_Lower + Interval_Upper) / 2
        return x

    def Fibonacci(self, func, FinalRange, epsilon=0.1):
        fg_2 = 0
        fg_1 = 0
        fg   = 0
        g_2 = 0
        g_1 = 0
        g   = 0

        Interval_Upper = 0
        Interval_Lower = 0

        #Phase 1 Find Interval of Interest
        index = 2
        print('------------Phase 1 Start------------')
        while(True):
            if (index == 2):
                g_2 = self.__Step(0)
                g_1 = self.__Step(index-1)
                g   = self.__Step(index)

                fg_2 = func(0)
                fg_1 = func(g_1)
                fg   = func(g)

                if (fg_2 > fg_1 and fg_1 < fg):
                    Interval_Lower = 0
                    Interval_Upper = g
                    break
            else:
                g_2 = self.__Step(index-2)
                g_1 = self.__Step(index-1)
                g   = self.__Step(index)

                fg_2 = func(g_2)
                fg_1 = func(g_1)
                fg   = func(g)

                if (fg_2 > fg_1 and fg_1 < fg):
                    Interval_Lower = g_2
                    Interval_Upper = g
                    break

            index = index + 1

        self.__phase1Interval[0] = Interval_Lower
        self.__phase1Interval[1] = Interval_Upper

        print('Uncertainty Interval Lower: ', Interval_Lower , ' Upper: ', Interval_Upper)
        print('------------Phase 1 Done-------------')

        Interval = Interval_Upper - Interval_Lower
        if (Interval < FinalRange):
            x = (Interval_Upper + Interval_Lower)/2
            return x
        
        Iteration_N = 0
        while(True):
            Fn = FibSequence(Iteration_N+1)
            if (Fn >= (1+ 2* epsilon) * (Interval/FinalRange)):
               break
            Iteration_N = Iteration_N + 1

        print('------Start Iterate----- Steps: ', Iteration_N)

        alpha = 0
        beta = 0
        f_alpha = 0
        f_beta = 0
        bound = BoundaryChange.Nochange

        for index in range(0, Iteration_N):
            if (index == 0):
                rho = 1 - (FibSequence(Iteration_N) / FibSequence(Iteration_N+1))
                print('rho: ', rho)
                alpha = Interval_Lower + rho * Interval
                beta  = Interval_Lower + (1 - rho) * Interval
                f_alpha = func(alpha)
                f_beta  = func(beta)
                if (f_alpha < f_beta):
                    Interval_Upper = beta
                    bound = BoundaryChange.Upper
                    print('Upper Changed, Upper: ', Interval_Upper)
                elif (f_alpha > f_beta):
                    Interval_Lower = alpha
                    bound = BoundaryChange.Lower
                    print('Lower Changed, Lower: ', Interval_Lower)
                else:
                    Interval_Lower = alpha
                    Interval_Upper = beta
                    bound = BoundaryChange.Both
                    print('Both Changed, Lower: ', Interval_Lower, ' ,Upper: ', Interval_Upper)
                
                Interval = Interval_Upper - Interval_Lower

            elif (index == (Iteration_N-1)):
                rho = 0.5 - epsilon/2
                print('rho: ', rho)
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = Interval_Lower + (1 - rho) * Interval
                    f_beta = func(beta)

                elif(bound == BoundaryChange.Upper):
                    beta = alpha
                    f_beta = f_alpha
                    alpha = Interval_Lower + rho * Interval
                    f_alpha = func(alpha)

                else:
                    alpha = Interval_Lower + rho * Interval
                    beta  = Interval_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                    f_beta  = func(beta)

                if (f_alpha < f_beta):
                    Interval_Upper = beta
                    bound = BoundaryChange.Upper
                    print('Upper Changed, Upper: ', Interval_Upper)
                elif(f_alpha > f_beta):
                    Interval_Lower = alpha
                    bound = BoundaryChange.Lower
                    print('Lower Changed, Lower: ', Interval_Lower)
                else:
                    Interval_Lower = alpha
                    Interval_Upper = beta
                    bound = BoundaryChange.Both
                    print('Both Changed, Lower: ', Interval_Lower, ' ,Upper: ', Interval_Upper)

                Interval = Interval_Upper - Interval_Lower

            else:
                rho = 1 - (FibSequence(Iteration_N-index)/ FibSequence(Iteration_N-index+1))
                print('rho: ', rho)
                if (bound == BoundaryChange.Lower):
                    alpha = beta
                    f_alpha = f_beta
                    beta = Interval_Lower + (1 - rho) * Interval
                    f_beta = func(beta)

                elif(bound == BoundaryChange.Upper):
                    beta = alpha
                    f_beta = f_alpha
                    alpha = Interval_Lower + rho * Interval
                    f_alpha = func(alpha)

                else:
                    alpha = Interval_Lower + rho * Interval
                    beta  = Interval_Lower + (1 - rho) * Interval
                    f_alpha = func(alpha)
                    f_beta  = func(beta)

                if (f_alpha < f_beta):
                    Interval_Upper = beta
                    bound = BoundaryChange.Upper
                    print('Upper Changed, Upper: ', Interval_Upper)
                elif(f_alpha > f_beta):
                    Interval_Lower = alpha
                    bound = BoundaryChange.Lower
                    print('Lower Changed, Lower: ', Interval_Lower)
                else:
                    Interval_Lower = alpha
                    Interval_Upper = beta
                    bound = BoundaryChange.Both
                    print('Both Changed, Lower: ', Interval_Lower, ' ,Upper: ', Interval_Upper)

                Interval = Interval_Upper - Interval_Lower

        print('Uncertainty Interval Lower: ', Interval_Lower , ' Upper: ', Interval_Upper)
        print('Interval: ', Interval)
        print('------------Phase 2 Done------------')

        x = (Interval_Lower + Interval_Upper) / 2
        return x

    def GetPhase1Interval(self):
        return self.__phase1Interval
        
                        




