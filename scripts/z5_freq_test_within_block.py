import math
import scipy.special as spc
import argparse
import pandas as pd
import numpy as np
import glob


def ParseArguments():
    parser = argparse.ArgumentParser(description="Frequency test within block")
    parser.add_argument('--input-file', default="generated_numbers.pkl",
                        required=False, help='input file (default: %(default)s)')
    parser.add_argument('--block_size', default=10,
                        required=False, help='block_size for frequency test within block (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False,
                        help='output file with p-values (default: %(default)s)')

    args = parser.parse_args()

    return args.input_file, args.block_size, args.input_dir, args.pval_file


input_file, block_size, input_dir, pval_file = ParseArguments()



def int_to_bin(num):
    numbers = ''
    for i in num:
        bin = np.binary_repr(i)
        zeros = '0' * ((int(np.log2(M))) - len(bin))
        numbers = numbers + zeros + bin
    return numbers


def to_str(num):
    numbers = ''
    for i in range(len(num)):
        numbers = numbers + str(num[i])
    return numbers


def block_frequency(bin_data: str, block_size):
    M = len(bin_data)
    num_blocks = math.floor(M/block_size)  # ilość bloków
    block_start, block_end = 0, block_size
    proportion_sum = 0.0
    for i in range(num_blocks):
        block_data = bin_data[block_start:block_end]
        ones_count = 0
        for char in block_data:
            if char == '1':
                ones_count += 1
        pi = ones_count / block_size  # pi - proporcja jedynek w jednym bloku
        proportion_sum += pow(pi - 0.5, 2.0)  # suma( (pi-0.5)**2 )
        block_start += block_size
        block_end += block_size
    chi_squared = 2.0 * block_size * proportion_sum
    p_val = spc.gammaincc(num_blocks / 2, chi_squared)
    return p_val


if input_dir == "":  # one .pkl file

    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']

    n = int(numbers_info['n'])

    M = numbers_info['Modulus']

    numbers = numbers_info['numbers']
    if M != 2:
        numbers = int_to_bin(numbers)

    pval = block_frequency(numbers, block_size)

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
        if M != 2:
            numbers = int_to_bin(numbers)
        pval = block_frequency(numbers, block_size)
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
