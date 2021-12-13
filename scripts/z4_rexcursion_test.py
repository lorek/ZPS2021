import numpy as np
import scipy.special as sc
from scipy.stats import chisquare
import argparse
import pickle
import pandas as pd

import glob

# for now returns mean of p-values for x /in [-4,4]\{0}

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


def string_output(numbers):
    str_output = str()
    for i in range(len(numbers)):
        str_output = str_output + str(numbers[i])
    return str_output


# (0,1) -> (-1,+1)
def plus_minus_one(numbers):
    striing = string_output(numbers)
    return [2 * int(striing[i]) - 1 for i in range(len(striing))]


# converts decimal input to binary
def decimal_to_binary(n, M):
    bits = np.log2(M)
    binary_number = bin(n)[2:]
    while len(binary_number) < bits:
        binary_number = "0" + binary_number
    return binary_number


def pi_function(x):
    def pi_1234(k, x):
        return 1 / (4 * x ** 2) * (1 - 1 / (2 * abs(x))) ** (k - 1)

    pi = [pi_1234(k, x) for k in [1, 2, 3, 4]]
    pi = [1 - 1 / (2 * abs(x))] + pi + [1 / (2 * abs(x)) * (1 - 1 / (2 * abs(x))) ** 4]
    return np.array(pi)


def random_exc_test(numbers, M):
    numbers = [decimal_to_binary(number, M) for number in numbers]

    p_m = plus_minus_one(numbers)

    summary = list(np.cumsum(p_m))
    summary = [0] + summary + [0]

    J = summary.count(0) - 1

    if J < 500:
        raise ValueError("If J < 500, the test is discontinued in order to satisfy the empirical rule for Chi-square "
                         "computations. Bigger input needed.")
    # gets list of cycles
    cycles = []
    pos1, pos2 = 0, 0
    try:
        while True:
            pos1 = summary.index(0, pos1)
            pos2 = summary.index(0, pos1 + 1)
            cycles.append(summary[pos1:pos2 + 1])
            pos1 = pos2
    except:
        pass

    # table like the one at NIST 2.14.4 step (6)

    v = np.zeros((8, 6))

    # [-4, -3, -2, -1, 1, 2, 3, 4] -> [0, 1, 2, 3, 4, 5, 6, 7]
    x_to_index_dict = {-4: 0, -3: 1, -2: 2, -1: 3, 1: 4, 2: 5, 3: 6, 4: 7}
    # [0, 1, 2, 3, 4, 5, 6, 7] -> [-4, -3, -2, -1, 1, 2, 3, 4]

    # counts occurrence of values [-4, 4] \ {0} in every cycle
    # table like the one at NIST 2.14.4 step (5)

    auxiliary_matrix = np.array([[cycles[i].count(-4) for i in range(len(cycles))],
                                 [cycles[i].count(-3) for i in range(len(cycles))],
                                 [cycles[i].count(-2) for i in range(len(cycles))],
                                 [cycles[i].count(-1) for i in range(len(cycles))],
                                 [cycles[i].count(1) for i in range(len(cycles))],
                                 [cycles[i].count(2) for i in range(len(cycles))],
                                 [cycles[i].count(3) for i in range(len(cycles))],
                                 [cycles[i].count(4) for i in range(len(cycles))]])

    # the total number of cycles in which state x occurs exactly k times among all cycles
    # table like the one at NIST 2.14.4 step (6)
    for _ in range(8):
        v[_] = [list(auxiliary_matrix[_]).count(i) for i in range(6)]
        v[_][5] = sum(element >= 5 for element in list(auxiliary_matrix[_]))

    def chi_square(x):
        chi, p_value = chisquare(v[x_to_index_dict[x]], J * pi_function(x))
        return chi, p_value

    chi_square_values = [chi_square(k) for k in x_to_index_dict.keys()]
    return [chi_square_values[i][1] for i in range(8)]


if input_dir == "":  # one .pkl file

    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']

    n = int(numbers_info['n'])

    M = numbers_info['Modulus']

    numbers = numbers_info['numbers']

    pval = np.mean(random_exc_test(numbers, M))

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

        pval = np.mean(random_exc_test(numbers, M))
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
