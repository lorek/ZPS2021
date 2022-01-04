import math
import argparse
import pandas as pd
import numpy as np
import glob
from scipy.stats import poisson


def ParseArguments():
    parser = argparse.ArgumentParser(description="Bday Spacing Test")
    #parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl",
                        required=False, help='input .pkl file (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()


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

    p = 1 - poisson.cdf(K-0.01*K, l)

    return(p)


if input_dir == "":  # one .pkl file

    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']

    n = int(numbers_info['n'])

    M = numbers_info['Modulus']

    numbers = numbers_info['numbers']

    pval = bday_spac_test(M, numbers)

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
        pval = bday_spac_test(M, numbers)
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
#
