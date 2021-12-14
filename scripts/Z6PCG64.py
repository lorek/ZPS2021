import random
#import matplotlib.pyplot as plt
import time
import argparse
import pickle
import pandas as pd
import numpy as np
'''
def ParseArguments():
    parser = argparse.ArgumentParser(description="PCG64")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--s', required=False, help='seed in PRNG')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()
    return args.n, args.s, args.output_file
    
n, s, output_file = ParseArguments()'''

def ParseArguments():
    parser = argparse.ArgumentParser(description="LCG")
    parser.add_argument('--n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('--seeds', default="sample_seeds.csv", required=False,
                        help='File (.csv) with seeds (default: %(defaault)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--output-dir', default="numbers", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seeds, args.output_file, args.output_dir

from numpy.random import PCG64

n, seeds_file, output_file, output_dir = ParseArguments()
n = int(n)

if(seeds_file!=""):
	print("ASDF")
	df_seeds=pd.read_csv(seeds_file)
	seeds=df_seeds["seeds"].to_numpy()
else:
    seeds  = np.array([int(time.time())])
'''
if s:
    PCG64 = np.random.default_rng(np.random.PCG64(seed=s))
else: PCG64 = np.random.default_rng(np.random.PCG64(seed=int(time.time())))
'''
if (output_dir != ""):
    output_dir += "\\";
else:
    output_dir += "\\";
'''
numbers_PCG64 = PCG64.random(n)
numbers_PCG64 = numbers_PCG64 * 2**32
numbers_PCG64 = list(map(int, numbers_PCG64))

if output_file=="":
    print("Wygenerowane liczby: \n", numbers_PCG64)
else:
    data = {'PRNG': "PCG64:",
            'Modulus': 2 ** 32,
            'n' : n,
            'numbers': numbers_PCG64}
    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)
'''
if len(seeds) == 1:
    PCG64 = np.random.default_rng(np.random.PCG64(seed=seeds))
    pcg64_1 = PCG64.random(n)
    pcg64_1 = pcg64_1 * 2**32
    pcg64_1 = list(map(int, pcg64_1))
    if output_file == "":
        print("Wygenerowane liczby: \n", pcg64_1)
    else:
        data = {'PRNG': "PCG64:",
                'Modulus': 2 ** 32,
                'n': n,
                'numbers': pcg64_1}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)

else:  # jest wiecej seedow
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        PCG64 = np.random.default_rng(np.random.PCG64(seed=seed))
        pcg64_1 = PCG64.random(n)
        pcg64_1 = pcg64_1 * 2 ** 32
        pcg64_1 = list(map(int, pcg64_1))
        print(pcg64_1[:5])
        output_file = output_dir + output_file_prefix + "_seed_" + str(seed) + ".pkl"
        print(output_file)
        data = {'PRNG': "PCG64:",
                'Modulus': 2 ** 32,
                'n': n,
                'numbers': pcg64_1}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr. ", nr, ",\t", output_file)

