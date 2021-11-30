import scipy.stats as sts
import argparse
import pandas as pd
import numpy as np


# python  z4_ks_test.py --input-file lcg1_numbers.pkl

def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorow-Smirnow test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


def bits_to_decimal(numbers, Mo=10):
    n = len(numbers)
    result_list = [""] * ((n // Mo) + 1)
    for i in range(len(result_list) - 1):
        for j in range(Mo):
            result_list[i] += numbers[j]
        numbers = numbers[Mo:]
    for i in range(n % Mo):
        result_list[-1] += numbers[i]
    return [int(str(element), 2) for element in result_list]


input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

n = int(numbers_info['n'])

numbers = numbers_info['numbers'][:10000]
M = int(numbers_info['Modulus'])

print("M = ", M)
print("n = ", n)

print("5 first numbers: ", numbers[:5])

if M == 2: # nieudana próba przyjmowania binarnego wejścia
    res = [str(number) for number in numbers]
    numbers = bits_to_decimal(res)

numbers = list(map(lambda x: x / M, numbers))

test = sts.kstest(numbers, cdf="uniform")  # result: (statistic, p-value)

print("KOLMOGOROW-SMIRNOW TEST results:")
print("KS statistic = {ks}, p-value = {p}".format(ks=round(test[0], 4), p=round(test[1], 4)))
