import numpy as np
#import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import pandas as pd

def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorov-Smirnov Test")
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
numbers=[numbers[i]/M for i in range(n)]
print(numbers[:5])

from scipy.stats import kstest
stat, pvalue = kstest(numbers, cdf='uniform') #cdf='norm'
#print(pvalue)
print(kstest(numbers, cdf='uniform')) #cdf='norm'
if pvalue < 0.05: print("Random?: False")
else: print("Is random?: True")