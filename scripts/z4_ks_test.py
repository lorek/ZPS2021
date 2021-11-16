import scipy.stats as sts
import argparse
import pandas as pd


def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorow-Smirnow test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

n = int(numbers_info['n'])

numbers = numbers_info['numbers']

try:
    M = int(numbers_info['Modulus'])
except KeyError:
    if max(numbers) < 1:
        M = 1
    else:
        M = max(numbers)


print("M = ", M)
print("n = ", n)

print("5 first numbers: ", numbers[:5])

numbers = list(map(lambda x: x / M, numbers))

test = sts.kstest(numbers, cdf="uniform")  # result: (statistic, p-value)

print("KOLMOGOROW-SMIRNOW TEST results:")
print("KS statistic = {ks}, p-value = {p}".format(ks=round(test[0], 4), p=round(test[1], 4)))
