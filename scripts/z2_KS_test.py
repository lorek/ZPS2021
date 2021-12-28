from scipy.stats import kstest
import argparse
import pandas as pd
import numpy as np
import glob


def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorow-Smirnow test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--input-dir', default="numbers", required=False, help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False, help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()

if input_dir == "":
    numbers_info = pd.read_pickle(input_file)
    prng_info = numbers_info['PRNG']
    n = int(numbers_info['n'])
    M = numbers_info['Modulus']
    numbers = numbers_info['numbers']

    numbers = [numbers[i] / M for i in range(n)]  # Zamiana liczb na liczby  z (0,1)

    test = kstest(numbers, cdf='uniform')

    p_value = test[1]

    print("pval = ", np.round(p_value, 5))
    pvals = []
    pvals.append(p_value)
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

        numbers = [numbers[i] / M for i in range(n)]  # Zamiana liczb na liczby  z (0,1)

        test = kstest(numbers, cdf='uniform')

        p_value = test[1]
        pvals.append(p_value)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
