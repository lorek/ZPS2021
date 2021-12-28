import argparse
import pickle
import sympy
import random
import pandas as pd
import numpy as np
import time


def ParseArguments():
    parser = argparse.ArgumentParser(description="BBSG PRNG")
    parser.add_argument('--n', default="1000", required=False,
                        help='nr of generated bits (default: %(default)s)')
    parser.add_argument('--x', default=str(30**10), required=False,
                        help='parameter \'x_0\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--y', default=str(40**10), required=False,
                        help='parameter \'x_1\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    parser.add_argument('--output-dir', default="", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.x, args.y, args.output_file, args.seeds, args.output_dir


def bbsg(n, x, y, seed=random.randint(1, 1e10)):

    def next_usable_prime(x):
        p = sympy.nextprime(x)
        while p % 4 != 3:
            p = sympy.nextprime(p)
        return p

    random_numbers = []
    p = next_usable_prime(x)
    q = next_usable_prime(y)
    M = p * q
    for i in range(n):
        x = seed
        bit_output = ""
        for _ in range(n):
            x = x*x % M
            b = x % 2  # ostatni bit (reszty z dzielenia przez M w zapisie bin)
            bit_output += str(b)
    return bit_output


n, x, y, output_file, seeds_file, output_dir = ParseArguments()


if seeds_file != "":
    print("ASDF")
    df_seeds = pd.read_csv(seeds_file)
    seeds = df_seeds["seeds"].to_numpy()
else:
    seeds = np.array([int(time.time())])

n = int(n)
x = int(x)
y = int(y)
M = 2

if output_dir != "":
    output_dir += "/"

if len(seeds) == 1:
    numbers = bbsg(n, x, y)

    # jesli output_file jest pusty to wyswietl liczby, w p.p. zapisz je do pliku

    if output_file == "":
        print("Wygenerowane liczby: \n", bbsg)
    else:
        # tak dla .csv, ale bedziemy uzywali pickle()
        # np.savetxt(output_file,lcg1,delimiter=";")

        data = {'PRNG': "BBSG:  x=" + str(x) + ", y=" + str(y),
                'Modulus': M,
                'n': n,
                'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)

else:  # jest wiecej seedow
    # przygotujmy nazwe -- zostawiamy tekst przed ostatnia kropka (np. z "asdf.asf_afs.pkl" zostawi "asdfasf_afs")
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(
        output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        numbers = bbsg(n, x, y, seed)
        output_file = output_dir + output_file_prefix + \
            "_seed_" + str(nr) + ".pkl"

        data = {'PRNG': "BBSG:  x=" + str(x) + ", y=" + str(y),
                'Modulus': M,
                'n': n,
                'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr ", nr, ",\t", output_file)


