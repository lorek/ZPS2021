import math
import random
import argparse
import pickle


def bday_spac_test(n, lst):
    m = len(lst)
    space = []
    lst.sort()

    for i in range(1, m):
        space.append(lst[i] - lst[i-1])
    space.append(abs(n - lst[-1] + lst[0]))
    space.sort()

    K = abs(len(set(space)) - m)
    l = m**3/(4*n)

    def f(j): return (l**j/math.factorial(j))*math.e**(-l)
    p = 1 - sum([f(j) for j in range(K)])

    return(p)


if __name__ == '__main__':
    n = 2**64
    lst = []
    # for _ in range(2**24):
    #     lst.append(random.randint(0, n))

    # print(bday_spac_test(n, lst))
    lst = [24, 83, 79, 54, 57, 10, 38, 84, 27, 36]
    print(bday_spac_test(100, lst))
