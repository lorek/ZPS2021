import argparse
import pandas as pd
from scipy.stats import chisquare
import numpy as np
import glob


def ParseArguments():
    parser = argparse.ArgumentParser(description="Frequency of pairs test")
    parser.add_argument('--bins', default="16", required=False,help='nr of bins (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--input-dir', default="numbers", required=False, help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False, help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.bins, args.input_file, args.input_dir, args.pval_file


bins, input_file, input_dir, pval_file = ParseArguments()

bins = int(bins)

def make_pairs(u):
    lst = []
    for i in range(len(u)//2):
        lst.append((u[2*i], u[2*i+1]))
    return lst


def count(lst_of_pairs, bins_num):

    if bins_num**(1/2) != int(bins_num**(1/2)):
        raise ValueError("Zla liczba binow")

    n = int(bins_num ** (1/2))
    numbers_in_bins = [[0] * n for i in range(0, n)]

    for pair in lst_of_pairs:
        for i in range(0, n):
            if i/n < pair[0] <= (i+1)/n:
                for j in range(0, n):
                    if j/n < pair[1] <= (j+1)/n:
                        numbers_in_bins[i][j] += 1

    flat_list = [k for sublist in numbers_in_bins for k in sublist]
    return flat_list


def freq_of_pair(seq, nr_of_bins=16, M=2**10):
    numbers = [seq[i] / M for i in range(len(seq))]  # Zamiana liczb na liczby  z (0,1)

    pairs = make_pairs(numbers)

    result = count(pairs, nr_of_bins)

    bins_expect = [len(pairs) / nr_of_bins] * nr_of_bins
    bins_observed = result

    chi_square_stat, p_value = chisquare(bins_observed, bins_expect)

    return p_value


if input_dir == "":
    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']
    n = int(numbers_info['n'])
    M = numbers_info['Modulus']
    numbers = numbers_info['numbers']

    pval = freq_of_pair(numbers, bins, M=M)

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

        pval = freq_of_pair(numbers, bins, M=M)

        print("pval = ", np.round(pval, 5))
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)

