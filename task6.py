import random
import matplotlib.pyplot as plt

def BSC(X, e):
    if isinstance(X, str):
        X = [int(b) for b in X]
    B = []
    for i in range(len(X)):
        if e > random.random():
            B.append(1 - X[i])
        else:
            B.append(X[i])
    return B
 
def check(X, B):
    count = 0
    for i in range(len(X)):
        if B[i] != X[i]:
            count += 1
    return count
 
def task6():
    for a in range(100):
        countY = 0
        countZ = 0
        delta   = round(0.01 * (a + 1), 2)
        epsilon = round(0.01 * (a + 1), 2)
        rounds  = 20000
        for _ in range(rounds):
            X = [random.randint(0, 1) for _ in range(7)]
            Y = BSC(X, epsilon)
            Z = BSC(X, delta)
            countY += check(X, Y)
            countZ += check(X, Z)
        print("Y has an average of " + str(round(countY / (len(X) * rounds), 5)) +
              " errors with an epsilon of " + str(epsilon))
        print("Z has an average of " + str(round(countZ / (len(X) * rounds), 5)) +
              " errors with a delta of "   + str(delta))
        
if __name__ == "__main__":
    print("TASK 6 ")
    task6()