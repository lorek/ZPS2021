import random
#import matplotlib.pyplot as plt
import time
import argparse
import pickle
import pandas as pd
import numpy as np
'''
def ParseArguments():
    parser = argparse.ArgumentParser(description="LCG")
    parser.add_argument('--n', default="500", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('--X0', required=False,
                        help='seed in PRNG recursion')
    parser.add_argument('--a', default="1664525", required=False,
                        help='parameter \'a\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--b', default="1013904223", required=False,
                        help='parameter \'b\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--M', required=False, help='Modulus \'M\' in PRNG recursion (default: 2^32)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.X0, args.a, args.b, args.M, args.output_file
'''
def ParseArguments():
    parser = argparse.ArgumentParser(description="LCG")
    parser.add_argument('--n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('--seeds', default="sample_seeds.csv", required=False,
                        help='File (.csv) with seeds (default: %(default)s)')
    parser.add_argument('--a', default="1103515245", required=False,
                        help='parameter \'a\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--b', default="12345", required=False,
                        help='parameter \'b\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--M', required=False, help='Modulus \'M\' in PRNG recursion (default: 2^31)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--output-dir', default="numbers", required=False,
                        help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.seeds, args.a, args.b, args.M, args.output_file, args.output_dir

def LCG(n, X0=random.randint(0, 2 ** 31 - 1), a=1103515245, b=	12345, M=2 **31):
    randoms = []
    X0 = X0 % M
    randoms.append((a * X0 + b) % M)
    for i in range(0,n-1):
        randoms.append((a * randoms[i] + b) % M)
    return randoms
"""
zał. generatora:
X0: 0<=X0<M
M: M>0
a: 0<=a<M
b: 0<=b<M
W generattorze LCG ziarnem jest pierwszy wyraz - X0
za kazdym razem X0 jest losowane za pomoca funkcji random.randint()
"""
n, seeds_file, a, b, M, output_file, output_dir = ParseArguments()
n = int(n)
'''
if X0:
    X0 = int(X0)
else: X0 = int(time.time())
'''

if(seeds_file!=""):

    seeds = np.array([])
    df_seeds= []

    with pd.read_csv(seeds_file, chunksize=10) as reader:
        for chunk in reader:
            seeds = np.append(seeds, list(chunk["seeds"]))
else:
    seeds  = np.array([int(time.time())])
print(seeds)


a = int(a)
b = int(b)
if M:
    M = int(M)
else: M = 2 ** 31
'''
randoms = LCG(n, X0, a, b, M)
if output_file=="":
    print("Wygenerowane liczby: \n", randoms)
else:
    data = {'PRNG': "LCG: a="+str(a)+", b="+str(b),
            'Modulus' : M,
            'n' : n,
            'numbers': randoms}
    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)
'''
if (output_dir != ""):
    output_dir += "\\";
else:
    output_dir += "\\";
#print(output_dir)

if len(seeds) == 1:
    lcg1 = LCG(n, X0=seeds, a=a, b=b, M=M)
    if output_file == "":
        print("Wygenerowane liczby: \n", lcg1)
    else:
        data = {'PRNG': "LCG: a=" + str(a) + ", b=" + str(b),
                'Modulus': M,
                'n': n,
                'numbers': lcg1}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_file)

else:  # jest wiecej seedow
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list) - 1)])

    for nr, seed in enumerate(seeds):
        lcg = LCG(n, X0=seed, M=M, a=a, b=b)

        output_file = output_dir + output_file_prefix + "_seed_" + str(seed) + ".pkl"
        print(output_file)
        data = {'PRNG': "LCG: a=" + str(a) + ", b=" + str(b),
                'Modulus': M,
                'n': n,
                'numbers': lcg}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)

        print("Saving file nr. ", nr, ",\t", output_file)
#if __name__ == '__main__':
#   print(LCG(2))
