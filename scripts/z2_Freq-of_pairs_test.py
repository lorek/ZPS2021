import argparse
import pandas as pd
from scipy.stats import chisquare


def ParseArguments():
    parser = argparse.ArgumentParser(description="Frequency of pairs test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

n = int(numbers_info['n'])
numbers = numbers_info['numbers']


def transform(u):  # Zamiana liczb w liczby (0,1)
    D = max(u) + 1
    for i in range(len(u)):
        u[i] = u[i] / D
    return u


numbers = transform(numbers)
print(numbers)

r = n / 2  # liczba par
L = 3
k = L ** 2  # liczba binóww
EX = r / k  # oczekiwana liczba par w 1. binie


def make_pairs(u):
    lst = []
    for i in range(len(u) // 2):
        lst.append((u[2 * i], u[2 * i + 1]))
    return lst


pairs = make_pairs(numbers)
print(pairs)


def count(lst):
    bins = [0] * 9
    for i in lst:
        if i[0] < 0.333 and i[1] < 0.333:
            bins[0] += 1
        elif 0.666 > i[0] > 0.333 and i[1] < 0.333:
            bins[1] += 1
        elif 1 > i[0] > 0.666 and i[1] < 0.333:
            bins[2] += 1

        elif i[0] < 0.333 and i[1] < 0.666 and i[1] > 0.333:
            bins[3] += 1
        elif 0.666 > i[0] > 0.333 and 0.666 > i[1] > 0.333:
            bins[4] += 1
        elif 1 > i[0] > 0.666 and 0.666 > i[1] > 0.333:
            bins[5] += 1

        elif i[0] < 0.333 and 1 > i[1] > 0.666:
            bins[6] += 1
        elif 0.666 > i[0] > 0.333 and i[1] < 1 and i[1] > 0.666:
            bins[7] += 1
        elif 1 > i[0] > 0.666 and 1 > i[1] > 0.666:
            bins[8] += 1
    return bins


liczba_par = count(pairs)
print(liczba_par)

test = chisquare(liczba_par, ddof=k - 1)

#########
print("Frequency of pairs test")
print("EX:", EX)
print("sum of pairs in bins:", liczba_par)
print("p-value:", test[1])
print("Statistic:", test[0])

