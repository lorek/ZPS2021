import random as r
import argparse
import pickle
import pandas as pd
import numpy as np
import time


def ParseArguments():
    parser = argparse.ArgumentParser(description="RC4 PRNG")
    parser.add_argument('--n', default='500', required=False,
                        help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--M', default=str(2**21), required=False,
                        help='Modulus \'M\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--K', default=r.sample(range(10000000), k=100), required=False,
                        help='seed (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    parser.add_argument('--output-dir', default="", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.M, args.K, args.output_file, args.seeds, args.output_dir


n, M, K, output_file, seeds_file, output_dir = ParseArguments()

n = int(n)
M = int(M)


def RC4(n, M, K):

    def ksa(K):
        S = [i for i in range(M)]
        l = len(K)
        j = 0
        for i in range(M):
            j = (j + S[i] + K[i % l]) % M
            S[i], S[j] = S[j], S[i]
        return S

    def prga(n, M, S):
        x = []
        i, j = 0, 0
        for _ in range(n):
            i = (i + 1) % M
            j = (j + S[i]) % M
            S[i], S[j] = S[j], S[i]
            x.append(S[(S[i] + S[j]) % M])
        return x

    return prga(n, M, ksa(K))


if output_dir != "":
    output_dir += "/"

if seeds_file != "":
    print("ASDF")
    df_seeds = pd.read_csv(seeds_file)
    seeds = df_seeds["seeds"].to_numpy()
else:
    seeds = np.array([int(time.time())])

if len(seeds) == 1:
    K = [i for i in range(int(seeds))]
    numbers = RC4(n, M, K)

    # jesli output_file jest pusty, to wyswietl liczby, w p.p. zapisz je do pliku

    if output_file == "":
        print("Wygenerowane liczby: \n", RC4)
    else:
        # tak dla .csv, ale bedziemy uzywali pickle()
        # np.savetxt(output_file,lcg1,delimiter=";")

        data = {'PRNG': "RC4",
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
        K = [i for i in range(int(seed))]
        numbers = RC4(n, M, K)
        output_file = output_dir + output_file_prefix + \
            "_seed_" + str(nr) + ".pkl"

        data = {'PRNG': "RC4",
                'Modulus': M,
                'n': n,
                'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr ", nr, ",\t", output_file)
