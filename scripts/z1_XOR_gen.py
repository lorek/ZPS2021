'''
Implementation of Exclusive OR Pseudorandom Number Generator (XORG)

Output:
    sequence of n integers in range 0 ... 2^M - 1  saved in `output_file`
    If `output_dir` is provided and there are more than one seed, results are saved
    in `output_dir` in multiple files with indexes.

Parameters:
    n:         number of generated numbers
    M:         integer such that generated numbers are in range 0, ... 2^M - 1
    seeds:     csv file storing seeds in form of ints in range 0...2^127 - 1

Sample usage: 
python scripts/z1_XOR_gen.py --n 1000 --M 8 --seeds 'scripts_learn/sample_seeds.csv' --output-file 'results/z1_XORG_numbers.pkl'
'''
import numpy as np
import argparse
import pickle
from time import perf_counter as time
from z1_convert import *
import pandas as pd
import os
import shutil

def ParseArguments():
    parser = argparse.ArgumentParser(description = "XOR Psudorandom number generator")
    parser.add_argument('--n', default = "1000000", required = False, help = 'nr of generated numbers (default: %(default)s)')
    parser.add_argument('--M', default = "8", required = False, help = 'generate numbers in range 0, ... 2^M - 1 (default M: %(default)s)')
    parser.add_argument('--output-file', default = "z1_XORG_numbers_int.pkl", required = False, help='output file (default: %(default)s)')
    parser.add_argument('--output-dir', default = "results/z1_XORG_numbers_int", required = False, help='output dir (default: %(default)s)')
    parser.add_argument('--seeds', default = 'scripts_learn/sample_seeds.csv', required = False, help = 'File storing seed for generator (default: %(default)s)')
    args = parser.parse_args()

    return int(args.n), int(args.M), args.output_file, args.output_dir, args.seeds

def xor(a: int, b: int) -> int:
    if type(a) != int or type(b) != int:
        raise ValueError(f"a ({type(a)}) and b ({type(b)}) must be ints")
    
    if a not in [0,1] or b not in [0,1]:
        raise ValueError(f"a = {a} ({type(a)}) and b = {b} ({type(b)}) must be 0 or 1.")
    
    return int(a != b)

def XORG(n: int, M: int, seed: int) -> list:
    """Returns a list of n pseudo-random numbers from {0, ... 2^M- 1} generated with XOR PRNG."""
    needed_bits = n * M
    bits = list(map(int, ints_to_bits(seed, 127)))
    L = len(bits)

    print(f"Running XORG with {L}-bit seed:\n{seed}\n...")
    for i in range(needed_bits - L):
        bits.append(xor(bits[i], bits[-1]))
    
    bits = "".join(map(str, bits))
    print(f"Generated {len(bits)} pseudo-random bits.\nBits are now being converted to {n} integers from 0 ... {2**M - 1} ({M} bits per integer).\n...")
    numbers = bits_to_ints(bits, n)
    
    return numbers

if __name__ == '__main__':
    n, M, output_file, output_dir, seeds = ParseArguments()
    
    print(f"Clearing contents of {output_dir}...")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    if(seeds != ""):
        print(f"Reading seeds from {seeds}...")
        seeds = pd.read_csv(seeds)["seeds"].to_numpy()
    else:
        seeds  = np.array([int(time.time())])

    start = time()
    for id, seed in enumerate(seeds):
        numbers = XORG(n, M, seed)
    
        data = {
            'PRNG': 'XORG', 
            'n' : n, 
            'max_int': 2**M - 1, 
            'seed': seed, 
            'numbers': numbers
            }
        
        prefix, ext = output_file.split(".")
        output_path = f"{output_dir}/{prefix}_{id}.{ext}"   
        
        with open(output_path, 'wb') as out: 
            pickle.dump(data, out)
    
    stop = time()
    print(f'Generated {n*len(seeds)} numbers in {(stop-start):.3}s.') 

