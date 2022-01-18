import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import glob, os
import pandas as pd
from math import sqrt, erfc

def rd(e): # funkcja zliczajaca serie
    liczba_serii = 1 # zawsze jest minimmum jedna seria
    n = len(e)
    for k in range(0, n - 1):
        if e[k] == e[k + 1]:
            continue
        else:
            liczba_serii += 1
    return liczba_serii
def changeNumbers(numbers, N = 31): # funkcja zamieniająca na zapis binarny
    e = []
    for i in range(0, len(numbers)):
        e.append(list(np.binary_repr(int(numbers[i]), N)))
    e1 = []
    for i in range(0, len(e)):
        for j in range(0, len(e[i])):
            e1 += e[i][j]
    e1 = list(map(int, e1))
    return e1
def help_function(e): # w argumencie changenumbers()!!!! # szybciej bedzie
    a = len(e)
    b = sum(e)
    c = rd(e)
    return {"sum": b, "length": a, "series": c}


def runs_test(dic):
    v = dic["series"]
    n = dic["length"]
    sum = dic["sum"]
    pi = sum / n
    r = 2 / sqrt(n)
    # print("pi: ", pi )
    # print("r: ", r)
    if abs(pi - 1 / 2) >= r:
        p_value = 0  # the test isn't run
    else:
        p_value = erfc(abs(v - 2 * n * pi * (1 - pi)) / (2 * sqrt(2 * n) * pi * (1 - pi)))
    return p_value


'''
def ParseArguments():
    parser = argparse.ArgumentParser(description="Runs Test")
    #parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()
    return args.input_file
input_file = ParseArguments()
'''


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    # parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='input .pkl file (default: %(default)s)')
    parser.add_argument('--input-dir', default="numbers", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="pvlcgruns.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()

if input_dir == "":  # one .pkl file

    numbers_info = pd.read_pickle(input_file)
    prng_info = numbers_info['PRNG']
    n = int(numbers_info['n'])
    M = int(numbers_info['Modulus'])
    numbers = numbers_info['numbers']
    #numbers = changeNumbers(numbers, N=M)
    dic = help_function(changeNumbers(numbers))
    pval = runs_test(dic)

    print("pval = ", np.round(pval, 5))
    pvals = []
    pvals.append(pval)
    print("Saving p-value to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file)

else:  # many .pkl files
    print("input_dir = ", input_dir)
    pvals = []
    file_list = list((glob.glob(input_dir + "\\**.pkl")))
    file_list.sort()
    for file_name in file_list:
        print("Processing file ", file_name, " ...")
        numbers_info = pd.read_pickle(file_name)

        prng_info = numbers_info['PRNG']
        n = int(numbers_info['n'])
        M = int(numbers_info['Modulus'])
        numbers = numbers_info['numbers']
        #numbers = changeNumbers(numbers)
        print(numbers[:5])
        dic = help_function(changeNumbers(numbers))
        print(dic)
        pval = runs_test(dic)
        print(pval)
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
print("PRNG = ", prng_info)
print("n = ", n)
print("M = ", M)
print("5 first numbers: ", numbers[:5])
'''
"""
from math import sqrt, erfc


def israndom(p_value):
    if p_value < 0.01:
        return False
    if p_value >= 0.01:
        return True
"""
# print("P_value: ", runs_test(e))
# print("Is random?: ",israndom(runs_test(e)))
# runs_test(e)