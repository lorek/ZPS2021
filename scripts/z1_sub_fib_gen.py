import numpy as np
import time

import argparse

import pickle


# Sample usage:
# python scripts_learn/fib_sub_gen.py --n 1000 --Mp 30 --k 100 --l 37 --seed seeds.txt --output-file results/sub_fib_numbers.pkl

def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--Mp', default="30", required=False, help='power of 2 in parameter M (default: %(default)s)')
    parser.add_argument('--k', default="100", required=False, help='value of k parameter (default: %(default)s)')
    parser.add_argument('--l', default="37", required=False, help='value of l parameter (default: %(default)s)')
    parser.add_argument('--seed', default="", required=False, help='name of the txt file with seed (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.Mp, args.k, args.l, args.seed, args.output_file


# funkcje

#LCG na potrzeby nie podania ziarna
def LCG(n):
    seed = int(time.time())
    a = 7 ** 5
    c = 0
    M = 2 ** 31 - 1
    result = [seed % M]
    for i in range(1, n):
        result.append((a * result[i-1] + c) % M)
    return result


#subtractive lagged fibbonaci generator
def sub_fib_gen(seed, gen=10, k=100, l=37, m=2**30):
    result = seed
    for i in range(len(seed)-1, len(seed) + gen, 1):
        result.append((result[i-k] - result[i-l]) % m)
    return result[-gen:]

# parametry z ParseArguments()

n, M, k, l, seed_name, output_file = ParseArguments()

n = int(n)
M = 2 ** int(M)
k = int(k)
l= int(l)

seed = []
if (seed_name == ""):
    seed = LCG(max(k,l))
else:
    seed_file = open(seed_name, "r")
    seed = list(map(int, seed_file.read().splitlines()))
    seed_file.close()


#generowanie
sub_fib = sub_fib_gen(seed, n, k, l, M)

# jesli output_file jest pusty, to wyswietl liczby, w przeciwnym przypadku zapisz je do pliku


if output_file == "":
    print("Wygenerowane liczby: \n", sub_fib)
else:

    data = {'PRNG': "sub_fib:  k=" + str(k) + ", l=" + str(l),
            'Modulus': M,
            'n': n,
            'seed': seed,
            'numbers': sub_fib}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)