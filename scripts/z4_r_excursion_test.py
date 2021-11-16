import numpy as np
import scipy.special as sc
import argparse
import pickle
import pandas as pd
import matplotlib.pyplot as plt

def ParseArguments():
    parser = argparse.ArgumentParser(description="Random excursion test")
    parser.add_argument('--input-file', default="binary_expansion_e.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


def string_output(numbers):
    str_output = str()
    for i in range(len(numbers)):
        str_output = str_output + str(numbers[i])
    return str_output


def plus_minus_one(numbers):
    striing = string_output(numbers)
    return [2 * int(striing[i]) - 1 for i in range(len(striing))]


input_file = ParseArguments()

numbers_info = pd.read_pickle(ParseArguments())

M = numbers_info['Modulus']
n = int(numbers_info['n'])

numbers = numbers_info['numbers']

print("M = ", M)
print("n = ", n)
print("10 first numbers: ", numbers[:10])

summary = [0]
p_m = plus_minus_one(numbers)

for i in range(len(p_m)):
    summary.append(summary[-1] + p_m[i])
summary.append(0)

x = list(range(len(summary)))

#plt.plot(x, summary, color="green")
#plt.xlim(0, n)
#plt.axhline(y=0, color="red")
#plt.show()

J = summary.count(0) - 1
print("J = ", J)

if J < 500:
    raise ValueError("If J < 500, discontinue the test in order to satisfy the empirical rule for Chi-square "
                     "computations.")

cycles = []
get_cycles = summary.copy()

while get_cycles.count(0) > 1:
    first_zero_index = get_cycles.index(0)
    second_zero_index = get_cycles[first_zero_index + 1:].index(0) + first_zero_index + 1
    cycle = get_cycles[first_zero_index + 1:second_zero_index]
    cycles.append(cycle)
    get_cycles = get_cycles[second_zero_index:]


def pi_function(k, x):
    if k == 0:
        return 1 - 1 / (2 * abs(x))
    elif k in [1, 2, 3, 4]:
        return 1 / (4 * x ** 2) * (1 - 1 / (2 * abs(x))) ** (k - 1)
    else:
        return 1 / (2 * abs(x)) * (1 - 1 / (2 * abs(x))) ** 4


# table like the one at NIST 2.14.4 step (6)

nr_of_cycles = 6
v = np.zeros((8, nr_of_cycles))

x_to_index_dict = {-4: 0, -3: 1, -2: 2, -1: 3, 1: 4, 2: 5, 3: 6, 4: 7}
reversed_dict = {v: k for k, v in x_to_index_dict.items()}

auxiliary_matrix = np.array([[cycles[i].count(-4) for i in range(len(cycles))],
                             [cycles[i].count(-3) for i in range(len(cycles))],
                             [cycles[i].count(-2) for i in range(len(cycles))],
                             [cycles[i].count(-1) for i in range(len(cycles))],
                             [cycles[i].count(1) for i in range(len(cycles))],
                             [cycles[i].count(2) for i in range(len(cycles))],
                             [cycles[i].count(3) for i in range(len(cycles))],
                             [cycles[i].count(4) for i in range(len(cycles))]])

for _ in range(8):
    v[_] = [list(auxiliary_matrix[_]).count(i) for i in range(nr_of_cycles)]


def chi_square(x):
    chi = [(v[x_to_index_dict[x]][k] - J * pi_function(k, x)) ** 2 / (J * pi_function(k, x)) for k in
           range(nr_of_cycles)]
    return sum(chi)


chi_square_values = [chi_square(k) for k in x_to_index_dict.keys()]


def p_values(chi_square_vals):
    chi_div_by_2 = [el / 2 for el in chi_square_vals]
    igamc_list = sc.gammainc(2.5, chi_div_by_2)
    return [1 - element for element in igamc_list]


print("RANDOM EXCURSION TEST result:")
for i in range(8):
    print("for state x = {x}: chi square = {c}, "
          "p-value = {p}".format(x=reversed_dict[i], c=round(chi_square_values[i], 4),
                                 p=round(p_values(chi_square_values)[i], 4)))

print("The p-value in every state should be >= 0.01 - only then we can assume that the sequence is random.")
