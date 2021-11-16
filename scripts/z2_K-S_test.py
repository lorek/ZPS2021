from scipy.stats import kstest
import argparse
import pandas as pd
import pickle

def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorow-Smirnow test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()


numbers_info = pd.read_pickle(input_file)
numbers = numbers_info['numbers']

def transform(u):
    D = max(u) + 1
    for i in range(len(u)):
        u[i] = u[i]/D
    return u


numbers = transform(numbers)

test = kstest(numbers, cdf='uniform')


print("Kolmogorow-Smirnow test:")
print("p-value:", test[1])
print("Statistic:", test[0])
