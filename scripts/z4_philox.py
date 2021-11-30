import numpy as np
import time
import argparse
import pickle
from numpy.random import Philox


#  python z4_philox_prng.py --output-file philox_numbers.pkl


def ParseArguments():
    parser = argparse.ArgumentParser(description="Philox PRNG")
    parser.add_argument('--n', default="1000", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--M', default="1024", required=False)
    parser.add_argument('--s', required=False)
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')

    args = parser.parse_args()

    return args.n, args.M, args.s, args.output_file


n, M, s1, output_file = ParseArguments()

n = int(n)
M = int(M)

if s1:
    s = s1
else:
    s = int(time.time())

rng_philox = np.random.default_rng(np.random.Philox(seed=s))

numbers_philox_01 = rng_philox.random(n)
numbers_philox = [int(number * M) for number in numbers_philox_01]

if output_file == "":
    print("Wygenerowane liczby: \n", numbers_philox)
else:
    data = {'PRNG': "Philox",
            'n': n,
            'Modulus': M,
            'numbers': numbers_philox}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)

    print("Wygenerowane liczby zapisano w: ", output_file)
