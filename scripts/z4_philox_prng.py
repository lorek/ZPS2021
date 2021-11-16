import numpy as np
import time
import argparse
import pickle
from numpy.random import Philox


def ParseArguments():
    parser = argparse.ArgumentParser(description="Philox PRNG")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')

    args = parser.parse_args()

    return args.n, args.output_file


n, output_file = ParseArguments()

n = int(n)

s = int(time.time())

rng_philox = np.random.default_rng(np.random.Philox(seed=s))

numbers_philox = rng_philox.random(n)

if output_file == "":
    print("Wygenerowane liczby: \n", numbers_philox)
else:
    data = {'PRNG': "Philox",
            'n': n,
            'numbers': numbers_philox}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)

    print("Wygenerowane liczby zapisano w: ", output_file)
