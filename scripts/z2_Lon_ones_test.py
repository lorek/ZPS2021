import argparse
import pandas as pd
from scipy.special import gammaincc
import numpy as np
import glob
import math


def ParseArguments():
    parser = argparse.ArgumentParser(description="Test for the longest runs in block")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--input-dir', default="numbers", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()

'''
def seq_of_binary(lst, n):  # n oznacza ile chcemy znakow w zapisie binarnym liczby
    seq = ''
    for i in range(len(lst)):
        binary = bin(lst[i])[2:]

        if len(binary) > n:
            raise ValueError("Za duza liczba!")

        while len(binary) < n:
            binary = '0' + binary

        seq = seq + binary
    return seq
'''

def divide_bin(n, binary):  # Tworzy bloki n-liczbowe?
    lst = []
    while binary != '':
        lst.append(binary[0:n])
        binary = binary[n:]
    return lst


def longest_block(lst):  # Liczy ile maksymalnie 1. występuje najwięcej obok siebie
    max_list = []
    for seq in lst:
        k = 0
        blocks_lengths = []

        for i in range(len(seq)):
            if seq[i] == '1':
                k += 1
            if seq[i] == '0':
                blocks_lengths.append(k)
                k = 0
        blocks_lengths.append(k)
        max_list.append(max(blocks_lengths))

    return max_list


def lon_ones(seq, M):

    binary = ''

    nr_digits = int(np.log2(M))

    for nr in seq:
        nr_binary_text = np.binary_repr(nr, nr_digits)
        binary += nr_binary_text

    if len(binary) < 128:
        print("Not enough data to run the test.")

    elif len(binary) < 6772:
        M = 8   # length of each block
        K = 3   # value of K
        N = math.floor(len(binary) / M)   # number of blocks

        binary_list = divide_bin(M, binary)
        max_ones = longest_block(binary_list)

        v = [0] * 4
        for i in max_ones:
            if i <= 1:
                v[0] += 1
            if i == 2:
                v[1] += 1
            if i == 3:
                v[2] += 1
            if i >= 4:
                v[3] += 1

        pi = [0.2148, 0.3672, 0.2305, 0.1875]
        chi = 0

        for i in range(K + 1):
            chi += (v[i] - N * pi[i]) ** 2 / (N * pi[i])

        p_value = gammaincc(K / 2, chi / 2)

        return p_value

    elif len(binary) < 750000:
        M = 128
        K = 5
        N = math.floor(len(binary) / M)

        binary_list = divide_bin(M, binary)
        max_ones = longest_block(binary_list)

        v = [0] * 6
        for i in max_ones:
            if i <= 4:
                v[0] += 1
            if i == 5:
                v[1] += 1
            if i == 6:
                v[2] += 1
            if i == 7:
                v[3] += 1
            if i == 8:
                v[4] += 1
            if i >= 9:
                v[5] += 1

        pi = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        chi = 0

        for i in range(K + 1):
            chi += (v[i] - N * pi[i]) ** 2 / (N * pi[i])
        p_value = gammaincc(K / 2, chi / 2)

        return p_value

    else:
        M = 10 ** 4
        K = 6
        N = math.floor(len(binary) / M)

        binary_list = divide_bin(M, binary)
        max_ones = longest_block(binary_list)

        v = [0] * 7
        for i in max_ones:
            if i <= 10:
                v[0] += 1
            if i == 11:
                v[1] += 1
            if i == 12:
                v[2] += 1
            if i == 13:
                v[3] += 1
            if i == 14:
                v[4] += 1
            if i == 15:
                v[5] += 1
            if i >= 16:
                v[6] += 1

        pi = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
        chi = 0

        for i in range(K + 1):
            chi += (v[i] - N * pi[i]) ** 2 / (N * pi[i])
        p_value = gammaincc(K / 2, chi / 2)

        return p_value


if input_dir == "":
    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']
    n = int(numbers_info['n'])
    M = numbers_info['Modulus']
    numbers = numbers_info['numbers']

    pval = lon_ones(numbers, M)

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

        numbers_info = pd.read_pickle(input_file)

        prng_info = numbers_info['PRNG']
        n = int(numbers_info['n'])
        M = numbers_info['Modulus']
        numbers = numbers_info['numbers']

        pval = lon_ones(numbers, M)

        print("pval = ", np.round(pval, 5))
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
