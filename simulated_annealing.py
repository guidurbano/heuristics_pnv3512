import random
import numpy as np
import time

class solution:
    def __init__(self, iter, x, T, ObjVal):
        self.iter = iter
        self.x = x
        self.T = T
        self.ObjVal = ObjVal


def main():
    for repl in range(1, 31):
        start = time.time()
        # Parameters
        alpha_nusp = 5  # 8
        alpha = 0.9
        x = 3 + 0.1 * alpha_nusp
        M = 50
        N = 50
        T0 = 1000
        k = 0.1
        solutions = []

        for i in range(0, M):
            for j in range(0, N):
                if j == 0:
                    best_solution = solution(iter=i,
                                             x=x,
                                             T=T0,
                                             ObjVal=2*x**6+3*x**4-12*x)

                rnd_x1 = random.random()
                rnd_x2 = random.random()
                step_size_x = 0
                if rnd_x1 > 0.5:
                    step_size_x = k * rnd_x2
                else:
                    step_size_x = - k * rnd_x2

                x1 = x + step_size_x
                ObjVal = 2*x**6+3*x**4-12*x
                ObjVal1 = 2*x1**6+3*x1**4-12*x1
                if ObjVal1 < ObjVal:
                    x = x1
                    if ObjVal1 < best_solution.ObjVal:
                        best_solution.iter = i
                        best_solution.x = x
                        best_solution.T = T0
                        best_solution.ObjVal = ObjVal1
                else:
                    rnd = random.random()
                    formula = np.exp(-(ObjVal1 - ObjVal) / T0)
                    if rnd < formula:
                        x = x1

            solutions.append(best_solution)
            T0 = T0 * alpha

        min = 10000000
        iMin = 0
        for i in range(0, M):
            if solutions[i].ObjVal < min:
                min = solutions[i].ObjVal
                iMin = i
            #print(f'Iter: {solutions[i].iter}, x: {solutions[i].x}, T: {solutions[i].T}, ObjVal: {solutions[i].ObjVal}')
        end = time.time()
        print(f'Repl: {repl}, Iter: {solutions[iMin].iter}, x: {solutions[iMin].x}, ObjVal: {solutions[iMin].ObjVal}, Time: {end-start}')


if __name__ == "__main__":
    main()
