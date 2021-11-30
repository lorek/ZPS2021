import math
import random
import argparse
import pickle
import pandas as pd


def ParseArguments():
    parser = argparse.ArgumentParser(description="Birthday Spacing Test")
    parser.add_argument('--input-file', default="generated_numbers.pkl",
                        required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)
n = int(numbers_info['n'])
M = numbers_info['Modulus']
numbers = numbers_info['numbers']


def bday_spac_test(M, numbers):
    num = numbers
    n = len(num)
    space = []
    num.sort()

    for i in range(1, n):
        space.append(num[i] - num[i-1])
    space.append(abs(M - num[-1] + num[0]))
    space.sort()

    K = abs(len(set(space)) - n)
    l = n**3/(4*M)

    def f(j): return (l**j/math.factorial(j))*math.e**(-l)
    p = 1 - sum([f(j) for j in range(K)])

    return(p)


print('BIRTHDAY SPACING TEST')
print("n = ", n)
print("M = ", M)
print("5 first numbers: ", numbers[:5])
print('p-value: ', bday_spac_test(M, numbers))
