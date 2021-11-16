import argparse
import pandas as pd
from scipy.special import gammaincc


def ParseArguments():
    parser = argparse.ArgumentParser(description="Test for the longest runs in block")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

numbers = numbers_info['numbers']


def seq_of_binary(num):   # Zamienia liczby na ciąg liczb binarnych
    seq = ''
    for i in range(len(num)):
        seq = seq + str(bin(num[i])[2:])
    return seq


binary = seq_of_binary(numbers)


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


if len(binary) < 128:
    print("Not enough data to run the test.")
elif len(binary) < 6772:
    M = 8
    K = 3
    N = 16
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
elif len(binary) < 750000:   #???
    M, K, N = 128, 5, 49
    binary_list = divide_bin(M, binary)
    max_ones = longest_block(binary_list)

    v = [0]*6
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
else:
    M, K, N = 10**4, 6, 75
    binary_list = divide_bin(M, binary)
    max_ones = longest_block(binary_list)

    v = [0]*7
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

#########
print("Test for the longest run of ones in block")
print("p-value:", p_value)
print("If the p-value is >= 0.01, the conclusion is that the sequence is random. Otherwise sequence is not random.")





