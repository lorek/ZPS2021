import numpy as np
#import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import pandas as pd
from scipy.stats import chisquare

def ParseArguments():
    parser = argparse.ArgumentParser(description="Frequency Test")
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
#numbers=[11100101]*50+ [234324234]*50
print("PRNG = ", prng_info)
print("n = ", n)
print("M = ", M)
print("5 first numbers: ", numbers[:5])


from math import sqrt, erfc

def changeNumbers(numbers):
    max_number=max(numbers)
    for i in range(0,len(numbers)):
        numbers[i]= numbers[i]/M
    return numbers

e = changeNumbers(numbers)
L = 2**8

def freq_test(numbers):
    print(numbers[1:5])
    a = []
    for i in range(0, L):
        a.append(0)

    for i in range(0, L):
        for j in range(0, len(numbers)):
            if numbers[j] >= i / L and numbers[j] < (i + 1) / L:
                a[i] = a[i] + 1
    print(a)
    print(chisquare(a,ddof=1))
    p_value = chisquare(a,ddof=1)[1]
    test_stat = chisquare(a,ddof=1)[0]
    return p_value, test_stat

def israndom(p_value):
    if p_value < 0.01:
        return False
    if p_value >= 0.01:
        return True

a = freq_test(numbers)
print(a)

