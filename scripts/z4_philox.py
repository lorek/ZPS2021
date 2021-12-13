import numpy as np

import time
from numpy.random import Philox
import pandas as pd

import argparse

import pickle

def ParseArguments():
    parser = argparse.ArgumentParser(description="Philox PRNG")
    parser.add_argument('--n', default="10000", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--M', default="1024", required=False, help='modulus (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="", required=False, help='File (.csv) with seeds  (default: %(default)s)')
    parser.add_argument('--output-dir', default="", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.M, args.output_file, args.seeds, args.output_dir


def my_philox(n, s, M):
    rng_philox = np.random.default_rng(np.random.Philox(seed=s))

    numbers_philox_01 = rng_philox.random(n)
    numbers_philox = [int(number * M) for number in numbers_philox_01]
    return numbers_philox


n, M, output_file, seeds_file, output_dir = ParseArguments()

n = int(n)
M = int(M)

if seeds_file != "":
    print("ASDF")
    df_seeds = pd.read_csv(seeds_file)
    seeds = df_seeds["seeds"].to_numpy()
else:
    seeds = np.array([int(time.time())])

if output_dir != "":
    output_dir += "/"

if len(seeds) == 1:
    generated = my_philox(n, seeds, M)

    if output_file == "":
        print("Wygenerowane liczby: \n", generated)
    else:
        data = {'PRNG': "Philox:",
                'Modulus': M,
                'n': n,
                'numbers': generated}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)

else:
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        generated = my_philox(n, seed, M)

        output_file = output_dir + output_file_prefix + "_seed_" + str(nr) + ".pkl"

        data = {'PRNG': "Philox:",
                'Modulus': M,
                'n': n,
                'numbers': generated}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr ", nr, ",\t", output_file)
