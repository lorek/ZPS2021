import argparse
import pickle
import time
import numpy as np
import pandas as pd


def ParseArguments():
    parser = argparse.ArgumentParser(description="QCG-I")
    parser.add_argument('--n', default="100", required=False,
                        help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--seeds', default="sample_seeds.csv", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    parser.add_argument('--p', default='5003', required=False,
                        help='Modulus \'p\' in PRNG recursion (default: 5003)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--output-dir', default="numbers", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seeds, args.p, args.output_file, args.output_dir


def QCG_I(n, seed, p=5003):
    numbers = [0]*n
    numbers[0] = (seed**2) % p
    for i in range(1, n):
        numbers[i] = (numbers[i-1]**2) % p
    return numbers


n, seeds_file, p, output_file, output_dir = ParseArguments()

n = int(n)
if p:
    p = int(p)
else:
    p = 5003

if seeds_file != "":
    print("ASDF")
    df_seeds = pd.read_csv(seeds_file)
    seeds = df_seeds["seeds"].to_numpy()
else:
    seeds = np.array([int(time.time())])

if output_dir != "":
    output_dir += "/"

if len(seeds) == 1:  #tylko 1 seed
    numbers = QCG_I(n, seeds[0], p)

    if output_file == "":
        print("Wygenerowane liczby: \n", numbers)
    else:

        data = {'PRNG': 'QCG-I',
                'seed': seeds[0],
                'Modulus': p,
                'n': n,
                'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)
else:  # jest wiecej seedow
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        numbers = QCG_I(n, seed, p)

        output_file = output_dir + output_file_prefix + "_seed_" + str(nr) + ".pkl"
        print(output_file)
        data = {'PRNG': 'QCG-I',
                'seed': seed,
                'Modulus': p,
                'n': n,
                'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr ", nr, ",\t", output_file)