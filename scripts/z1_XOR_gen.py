'''
Implementation of Exclusive OR Pseudorandom Number Generator (XORG)

Output:
    sequence of n integers in range 0 ... 2^M - 1  saved in `output_file`

Parameters:
    n:         number of generated numbers
    M:         integer such that generated numbers are in range 0, ... 2^M - 1
    seed_file: txt file storing sequence of first 127 bits (used to generate whole sequence) 

Sample usage: 
python scripts/z1_XOR_gen.py --n 1000 --M 8 --seed-file 'z1_XORG_seed.txt' --output-file 'results/z1_XORG_numbers.pkl'
'''
import numpy as np
import argparse
import pickle
from time import perf_counter as time
from z1_convert import *

def ParseArguments():
    parser = argparse.ArgumentParser(description = "XOR Psudorandom number generator")
    parser.add_argument('--n', default = "10000", required = False, help = 'nr of generated numbers (default: %(default)s)')
    parser.add_argument('--M', default = "8", required = False, help = 'generate numbers in range 0, ... 2^M - 1 (default M: %(default)s)')
    parser.add_argument('--output-file', default = "results/z1_XORG_numbers.pkl", required = False, help='output file (default: %(default)s)')
    parser.add_argument('--seed-file', default = "data/z1_XORG_seed.txt", required = False, help = 'File storing seed for generator (default: %(default)s)')
    args = parser.parse_args()

    return int(args.n), int(args.M), args.output_file, args.seed_file

def xor(a: int, b: int) -> int:
    if type(a) != int or type(b) != int:
        raise ValueError(f"a ({type(a)}) and b ({type(b)}) must be ints")
    
    if a not in [0,1] or b not in [0,1]:
        raise ValueError(f"a = {a} ({type(a)}) and b = {b} ({type(b)}) must be 0 or 1.")
    
    return int(a != b)

def XORG(n: int, M: int, seed: str) -> list:
    """Returns a list of n pseudo-random numbers from {0, ... 2^M- 1} generated with XOR PRNG."""
    needed_bits = n * M
    bits = [int(bit) for bit in seed]
    L = len(bits)

    print(f"Running XORG with {L}-bit seed:\n{seed}\n...")
    for i in range(needed_bits - L):
        bits.append(xor(bits[i], bits[-1]))
    
    bits = "".join(map(str, bits))
    print(f"Generated {len(bits)} pseudo-random bits.\nBits are now being converted to {n} integers from 0 ... {2**M - 1} ({M} bits per integer).\n...")
    numbers = bits_to_ints(bits, n)
    
    return numbers

if __name__ == '__main__':
    n, M, output_file, seed_file = ParseArguments()

    with open(seed_file, "r") as f:
        seed = f.readlines()[0]

    start = time()
    numbers = XORG(n, M, seed)
    stop = time()
    print(f'Generated {n} numbers in {(stop-start):.3}s.') 

    data = {'PRNG': 'XORG', 'n' : n, 'max_int': 2**M - 1, 'seed': seed, 'numbers': numbers}          
    with open(output_file, 'wb') as out: 
        pickle.dump(data, out)

    print(f"Results are saved in {output_file}.")
