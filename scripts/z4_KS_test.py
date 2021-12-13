import scipy.stats as sts
import argparse
import pandas as pd
import numpy as np
import glob


def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorow-Smirnow test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='input .pkl file (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False,
                        help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False,
                        help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()


def decimal_to_binary(n, M):
    bits = np.log2(M)
    binary_number = bin(n)[2:]
    while len(binary_number) < bits:
        binary_number = "0" + binary_number
    return binary_number


def converte(numbers, M, N=10):
    if M > 32:
        return numbers
    else:
        # zamiana na binary
        bin_string = "".join([decimal_to_binary(num, M) for num in numbers])
        parts_list = []
        while len(bin_string) > N:
            parts_list.append(bin_string[:N])
            bin_string = bin_string[N:]
        if len(bin_string) != 0:
            parts_list.append(bin_string)
        # na dec again
        decimal_list = [int(str(n), 2) for n in parts_list]
        return decimal_list


if input_dir == "":

    numbers_info = pd.read_pickle(input_file)

    prng_info = numbers_info['PRNG']

    n = int(numbers_info['n'])

    M = numbers_info['Modulus']

    numbers = converte(numbers_info['numbers'], M)

    numbers = list(map(lambda x: x / 2 ** 10, numbers))

    pval = sts.kstest(numbers, cdf="uniform")[1]

    print("pval = ", np.round(pval, 5))
    pvals = []
    pvals.append(pval)
    print("Saving p-value to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file)

else:
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
        numbers = converte(numbers_info['numbers'], M)

        numbers = list(map(lambda x: x / M, numbers))

        pval = sts.kstest(numbers, cdf="uniform")[1]
        pvals.append(pval)

    print("Saving p-values to ", pval_file)
    df = pd.DataFrame(pvals, columns=["p-value"])
    df.to_csv(pval_file, index=False)
