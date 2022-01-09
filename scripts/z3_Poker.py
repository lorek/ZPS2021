from scipy.special import comb
import numpy as np
import math
import argparse
import pandas as pd
from scipy.stats import chi2
import glob
import pickle


def PokerTest(n):

    k = len(n) // 3
    l = list(np.arange(0, k))
    n1 = n
    for i in range(0, k):
        while len(n1) > 0:
            l[i] = n1[:3]
            n1 = n1[3:]
            break

    s0 = s1 = s2 = s3 = 0
    for i in range(0, k):
        if l[i] == '000':
            s0 += 1
        if l[i] == '100':
            s1 += 1
        if l[i] == '001':
            s1 += 1
        if l[i] == '010':
            s1 += 1
        if l[i] == '110':
            s2 += 1
        if l[i] == '101':
            s2 += 1
        if l[i] == '011':
            s2 += 1
        if l[i] == '111':
            s3 += 1

    list_s = [s0, s1, s2, s3]

    b = []
    for i in range(0, 4):
        numerator = math.pow(list_s[i] - comb(3, i) * len(n) / ((2 ** 3) * 3), 2)/10
        denominator = comb(3, i) * len(n) / ((2 ** 3) * 3)
        N = numerator/denominator
        b.append(N)

    X2 = sum(b)
    X2theoretical = 7.81

    if X2 < X2theoretical:
        print('The sequence is random')
    else:
        print('The sequence is not random')

    p_value = chi2.sf(X2, 3)
    return (p_value)


def ParseArguments():
    parser = argparse.ArgumentParser(description="Poker Test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--input-dir', default="pickles_dir", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file

input_file, input_dir, pval_file = ParseArguments()


if input_dir=="":
    numbers_info = pd.read_pickle(input_file)
    n = int(numbers_info['n'])  # ilość liczb
    M = int(numbers_info['Modulus'])
    numbers_length = (M-1).bit_length() # długość liczb binarnie
    numbers = numbers_info['numbers']   # liczby (pseudolosowe)
    p_value = PokerTest(n)  # p-wartość

    print('Poker test results: ')
    print('p-value: ', str(p_value))
    print('Parameters:')
    print("M: " + str(numbers_info['Modulus']))
    print("n: " + str(numbers_info['n']))
    print("Numbers have been generated with: " + str(numbers_info['PRNG']))
    pvals = []
    pvals.append(p_value)
    print("Saving p-value to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)

else:
    print("input_dir = ", input_dir)
    pvals = []
    file_list = list((glob.glob(input_dir + "/**.pkl")))
    file_list.sort()
    for file_name in file_list:
        print("Processing file ", file_name, " ...")
        numbers_info = pd.read_pickle(file_name)
        n = int(numbers_info['n'])
        M = numbers_info['Modulus']
        numbers = numbers_info['numbers']
        numbers_length = (M - 1).bit_length()
        pval = PokerTest(n)
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
