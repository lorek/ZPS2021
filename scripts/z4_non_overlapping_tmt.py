import numpy as np
import matplotlib.pyplot as plt
import time
import random, re
import mpmath
from scipy.stats import norm
import argparse
import pickle
import pandas as pd
import textwrap
import glob, os

def ParseArguments():
    parser = argparse.ArgumentParser(description="Random excursion test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='input .pkl file (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()


def ints_into_bits(int_lst):
    seq = ''
    for i in range(len(int_lst)):
        seq = seq + str(bin(int_lst[i])[2:])
    return seq


# bits = ints_into_bits(generated_numbers)


def test(numbers, m=9, N=5):
    # numbers = list(numbers)
    str_of_bits = ints_into_bits(numbers)
    length = len(str_of_bits) # n
    template = format(random.getrandbits(m), "b").zfill(m)
    print("B = ", template)
    print("N = ", N)
    print("m = ", m)

    M = int(len(str_of_bits)/N)
    print(M, "długość bloków")
    blocks_lst = textwrap.wrap(str_of_bits, int(M))
    # print(blocks_lst)

    # parameters for the chi square test
    mi = (M - len(template) + 1)/pow(2, m)
    print("Średnia = ", mi)
    variance = M * (1 / pow(2, m) - (2 * m - 1.0) / pow(2, 2 * m))
    print("Wariancja = ",variance)
    # procesing
    # Wyliczenie W_j

    w_j = dict()
    i = 0

    for blocks in blocks_lst:
        count_pattern = len(re.findall(str(template), blocks))
        i += 1
        w_j[i] = count_pattern

    chi_sq = 0

    for j in range(1, N):
        chi_sq = chi_sq + pow((float(w_j[j]) - mi), 2) / variance

    p_value = (1/math.gamma(N/2)) * mpmath.gammainc(N / 2, chi_sq / 2)
    print("Statystyka chi-kwadrat = ", chi_sq)
    return round(p_value, 5)


if input_dir == "":  # one .pkl file

    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']

    n = int(numbers_info['n'])

    M = numbers_info['Modulus']

    numbers = numbers_info['numbers']

    pval = test(numbers)

    print("pval = ", np.round(pval, 5))
    pvals = []
    pvals.append(pval)
    print("Saving p-value to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file)

else:  # many .pkl files
    print("input_dir = ", input_dir)
    pvals = []
    file_list = list((glob.glob(input_dir + "/**.pkl")))
    file_list.sort()
    for file_name in file_list:
        print("Processing file ", file_name, " ...")
        numbers_info = pd.read_pickle(file_name)

        prng_info = numbers_info['PRNG']
        n = int(numbers_info['n'])
        M = numbers_info['Modulus']
        numbers = numbers_info['numbers']
        pval = test(numbers)
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)





