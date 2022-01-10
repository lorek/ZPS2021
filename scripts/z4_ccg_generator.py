
import time
import argparse
import pickle
import pandas as pd
import numpy as np


def ParseArguments():
    parser = argparse.ArgumentParser(description="CCG PRNG")
    parser.add_argument('--n', default="1000", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('--a', default="2", required=False,
                        help='parameter \'a\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--M', required=False, help='Modulus \'M\' in PRNG recursion (default: 634386549)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="", required=False, help='File (.csv) with seeds (default: %(default)s)')
    parser.add_argument('--output-dir', default="", required=False,
                        help='Directory to save .pkl files generated with seeds (default: %(default)s)')

    args = parser.parse_args()

    return args.n, args.a, args.M, args.output_file, args.seeds, args.output_dir



def CCG(n, seed, M, a = 2):
    numbers = [0] * n
    numbers[0] = seed % M
    for i in range(1,n):
        numbers[i] = (a*numbers[i-1]**3) % M

    return numbers


n, a, M, output_file, seeds_file, output_dir = ParseArguments()

n = int(n)
a = int(a)

if M:
    M = int(M)
else:
    M = 634386549


if (seeds_file != ""):
    print("ASDF")
    df_seeds = pd.read_csv(seeds_file)
    seeds = df_seeds["seeds"].to_numpy()
else:
    seeds = np.array([34])

if (output_dir != ""):
    output_dir += "\\"

if len(seeds) == 1:

    ccg1 = CCG(n, seeds[0], M)

    if output_file == "":
        print("Wygenerowane liczby: \n", ccg1)
    else:
        data = {'PRNG': "CCG: a=" + str(a),
                'Modulus': M,
                'n': n,
                'numbers': ccg1}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)

else:  # jest wiecej seedow
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        ccg1 = CCG(n, seed, M)

        output_file = output_dir + output_file_prefix + "_seed_" + str(nr) + ".pkl"

        data = {'PRNG': "CCG: a=" + str(a),
                'Modulus': M,
                'n': n,
                'numbers': ccg1}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr ", nr, ",\t", output_file)

