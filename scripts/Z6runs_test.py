import numpy as np
#import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import pandas as pd

def ParseArguments():
    parser = argparse.ArgumentParser(description="Runs Test")
    #parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file

input_file = ParseArguments()

numbers_info = pd.read_pickle(input_file)

prng_info = numbers_info['PRNG']
n=int(numbers_info['n'])
M= numbers_info['Modulus']
numbers = numbers_info['numbers']

print("PRNG = ", prng_info)
print("n = ", n)
print("M = ", M)
print("5 first numbers: ", numbers[:5])


from math import sqrt, erfc

N = 8
def changeNumbers(numbers):
    e = []
    for i in range(0,len(numbers)):
        a = np.binary_repr(numbers[i],N)
        e.append(list(a))

    e1 = []
    for i in range(0,len(e)):
        for j in range(0,len(e[i])):
            e1 += e[i][j]
    return e1

e = changeNumbers(numbers)
#print(e)


from math import sqrt, erfc



def r(e):
    sum2 = 0
    n = len(e)
    for k in range(0,n-1):
        if e[k] == e[k + 1]:
            continue
        else:
            sum2 += 1
    return sum2 + 1

v = r(e)

def runs_test(e):
    n = len(e)
    sum = 0
    for i in range(n):
        sum += int(e[i])
    pi = sum/n
    r = 2/sqrt(n)
    #print("pi: ", pi )
    #print("r: ", r)

    if abs(pi - 1/2) >= r:
        p_value = 0 #the test isn't run
    else:
        p_value = erfc(abs(v-2*n*pi*(1-pi))/(2*sqrt(2*n)*pi*(1-pi)))
    return p_value

def israndom(p_value):
    if p_value < 0.01:
        return False
    if p_value >= 0.01:
        return True

print("P_value: ", runs_test(e))
print("Is random?: ",israndom(runs_test(e)))


runs_test(e)
