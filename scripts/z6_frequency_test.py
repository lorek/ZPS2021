import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import glob, os
import pandas as pd
from scipy.stats import chisquare



# e = changeNumbers(numbers)
# L = 2**8
def freq_test(numbers, L=2 ** 4, M=2 ** 31):
    # numbers=changeNumbers(ints, M=M)
    #print(numbers[:5])
    a = [0] * L
    for i in range(0, L):
        for n in numbers:
            if (M / L * i) <= n < (M / L * (i + 1)):
                a[i] += 1
            if n == M:
                a[-1] += 1
    #print(a)
    # print(sum(a))
    # print(chisquare(a, ddof=0))
    p_value = chisquare(a)[1]
    print(p_value)
    # test_stat = chisquare(a, ddof=0)[0]
    return p_value  # , test_stat


'''
def ParseArguments():
    parser = argparse.ArgumentParser(description="Frequency Test")
    #parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()
    return args.input_file

input_file = ParseArguments()'''


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    # parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='input .pkl file (default: %(default)s)')
    parser.add_argument('--input-dir', default="numbers", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="pvlcgfreq.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()

if input_dir == "":  # one .pkl file

    numbers_info = pd.read_pickle(input_file)
    prng_info = numbers_info['PRNG']
    n = int(numbers_info['n'])
    M = numbers_info['Modulus']
    numbers = numbers_info['numbers']
    # print(numbers[:5])
    pval = freq_test(numbers, M=M)

    print("pval = ", np.round(pval, 5))
    pvals = []
    pvals.append(pval)
    print("Saving p-value to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file)

else:  # many .pkl files
    i = 0
    print("input_dir = ", input_dir)
    pvals = []
    file_list = list((glob.glob(input_dir + "\\**.pkl")))
    file_list.sort()
    for file_name in file_list:
        print("Processing file ", file_name, " ...")
        numbers_info = pd.read_pickle(file_name)
        i += 1
        prng_info = numbers_info['PRNG']
        n = int(numbers_info['n'])
        M = numbers_info['Modulus']
        numbers = numbers_info['numbers']
        # print(numbers[:5])
        pval = freq_test(numbers, M=M)
        print(i)
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)

'''
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

def israndom(p_value):
    if p_value < 0.01:
        return False
    if p_value >= 0.01:
        return True

a = freq_test(numbers)
print(israndom(a[0]))'''
