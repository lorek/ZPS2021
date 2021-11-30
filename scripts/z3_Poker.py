from scipy.special import comb
import numpy as np
from collections import Counter
import math
from scipy.stats import norm
import argparse
import pickle
import pandas as pd

def ParseArguments():
    parser = argparse.ArgumentParser(description="Poker Test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file

input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

prng_info = numbers_info['PRNG']
n = int(numbers_info['n'])

s = numbers_info['numbers']

def PokerTest(s,m):

    k = len(s) // m
    l = list(np.arange(0, k))
    s1 = s
    for i in range(0, k):
        while len(s1) > 0:
            l[i] = s1[:m]
            s1 = s1[m:]
            break
    n = l
    for j, i in enumerate(l):
        try:
            n[j] = Counter(i)['1']
        except:
            n[j] = Counter(i)['0']

    n.sort()
    niDict = dict(Counter(n))
    k = [i for i in range(0, m + 1)]
    mydict = dict(zip(k, [0] * len(k)))

    def check_existance(i, collection: iter):
        return i in collection

    if mydict.keys() == niDict.keys():
        print('ok')
    else:
        for i in mydict.keys():
            if check_existance(i, niDict.keys()) == False:
                niDict[i] = 0
    b = []

    for i in niDict.keys():
        numerator = math.pow(niDict[i] - comb(m, i) * len(s) / ((2 ** m) * m), 2)
        denominator = comb(m, i) * len(s) / ((2 ** m) * m)
        S = numerator / denominator
        b.append(S)

    X2 = sum(b)
    X2t = [3.84, 5.99, 7.81, 9.48, 11.07, 12.59, 14.06, 15.50, 16.91, 18.30]  # wartości z tabeli rozkładu
    if X2 < X2t[m-1]:
        print('The sequence is random')
    else:
        print('The sequence is not random')
    print('Chi square value: ',X2)
    print('Theoritical chi square value: ', X2t[m-1])

print(PokerTest(s,3))