import argparse
import pickle
import time
import pandas as pd
import numpy as np


def ParseArguments():
    parser = argparse.ArgumentParser(description="Fibonacci")
    parser.add_argument('--n', default="100", required=False,
                        help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--seeds', default="sample_seeds.csv", required=False,
                        help='File (.csv) with seeds  (''default: %(default)s)')
    parser.add_argument('--M', required=False,
                        help='Modulus \'M\' in PRNG recursion (default: 2**32)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: ''%(default)s)')
    parser.add_argument('--output-dir', default="numbers", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seeds, args.M, args.output_file, args.output_dir


def fibo_random_gen(n, seed1, M=2**32):
    numbers = [0] * (n+2)
    numbers[0] = seed1
    numbers[1] = seed1 % M
    for i in range(2, n+2):
        numbers[i] = (numbers[i-1]+numbers[i-2]) % M
    numbers = numbers[2:]
    return numbers


n, seeds_file, M, output_file, output_dir = ParseArguments()

n = int(n)
if M:
    M = int(M)
else:
    M = 2**32

if seeds_file != "":
    print("ASDF")
    df_seeds = pd.read_csv(seeds_file)
    seeds = df_seeds["seeds"].to_numpy()
else:
    seeds = np.array([int(time.time())])

if output_dir != "":
    output_dir += "/"

if len(seeds) == 1:  #tylko 1 seed
    numbers = fibo_random_gen(n, seeds[0], M)

    if output_file == "":
        print("Wygenerowane liczby: \n", numbers)
    else:

        data = {'PRNG': 'Fibonacci',
                'seed': seeds[0],
                'Modulus': M,
                'n': n,
                'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)
else:  # jest wiecej seedow
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        numbers = fibo_random_gen(n, seed, M)
        output_file = output_dir + output_file_prefix + "_seed_" + str(nr) + ".pkl"

        data = {'PRNG': 'Fibonacci',
                'seed': seed,
                'Modulus': M,
                'n': n,
                'numbers': numbers }

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr ", nr, ",\t", output_file)