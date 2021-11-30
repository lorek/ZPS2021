import math
import scipy.special as spc
import argparse
import pickle
import pandas as pd
import numpy as np


def ParseArguments():
    parser = argparse.ArgumentParser(description="Frequency test within block")
    parser.add_argument('--input-file', default="generated_numbers.pkl",
                        required=False, help='input file (default: %(default)s)')
    parser.add_argument('--block_size', default=10,
                        required=False, help='block_size for frequency test within block (default: %(default)s)')

    args = parser.parse_args()

    return args.input_file, args.block_size


input_file, block_size = ParseArguments()

numbers_info = pd.read_pickle(input_file)
n = int(numbers_info['n'])
M = numbers_info['Modulus']
numbers = numbers_info['numbers']
block_size = int(block_size)


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
    chi_squared = 4.0 * block_size * proportion_sum
    p_val = spc.gammaincc(num_blocks / 2, chi_squared / 2)
    return p_val


if M != 2:
    numbers = int_to_bin(numbers)


print('FREQUENCY TEST WITHIN A BLOCK')
print("n = ", n)
print("M = ", M)
print("5 first bits: ", numbers[:5])
print('p-value: ', block_frequency(to_str(numbers), block_size))
