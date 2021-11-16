import numpy as np
import time
import argparse
import pickle
import math



def ParseArguments():
    parser = argparse.ArgumentParser(description="CCG-generator")
    parser.add_argument('-n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('-a', default="2", required=False)
    parser.add_argument('-M', required=False)
    parser.add_argument('--seed', required=False, help='seed in PRNG recursion')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.a, args.M, args.seed, args.output_file



def CCG(n, seed, Modulus, a = 2):
    ccg = [0 for _ in range(n)]
    ccg[0] = seed % Modulus
    for i in range(1, n):
        ccg[i] = ((a * ccg[i-1]**3) % Modulus)

    return ccg


# parametry  ParseArguments()

n, a, M, s, output_file = ParseArguments()

n = int(n)
a = int(a)

if M:
    M = int(M)
else: M = 2**512

if s:
    s = int(s)
else: s = int(time.time())



ccg1 = CCG(n, s, M)

if output_file == "":
    print("Wygenerowane liczby: \n", ccg1)
else:

    data = {'PRNG': "CCG",
            'Modulus': M,
            'n': n,
            'numbers': ccg1}
    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)