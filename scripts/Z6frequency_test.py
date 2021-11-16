import numpy as np
#import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import pandas as pd

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

print("PRNG = ", prng_info)
print("n = ", n)
print("M = ", M)
print("5 first numbers: ", numbers[:5])


from math import sqrt, erfc

def changeNumbers(numbers):
    e = []
    for i in range(0,len(numbers)):
        a = str(bin(numbers[i]))
        e += a[2:]
        e = ''.join(e)
    return e

e = changeNumbers(numbers)

def freq_test(e):
    n = len(e)
    sn = 0
    for i in range(len(e)):
        if int(e[i]) == 1:
            sn += 1
        elif int(e[i]) == 0:
            sn += -1
    test_stat = abs(sn) / sqrt(n)
    p_value = erfc(test_stat / sqrt(2))

    return p_value

def israndom(p_value):
    if p_value < 0.01:
        return False
    if p_value >= 0.01:
        return True

print("P-value: ", freq_test(e))
print("Is random?: ", israndom((freq_test(e))))




