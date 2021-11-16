import numpy as np
import time
import argparse
import pickle


def ParseArguments():
    parser = argparse.ArgumentParser(description="PCG64")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--s', required=False, help='seed in PRNG')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')

    args = parser.parse_args()

    return args.n, args.s, args.output_file


n, s, output_file = ParseArguments()

n = int(n)

from numpy.random import PCG64

if s:
    PCG64 = np.random.default_rng(np.random.PCG64(seed=s))
else: PCG64 = np.random.default_rng(np.random.PCG64(seed=int(time.time())))

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
