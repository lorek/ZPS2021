"""
Implementation of Spacing Test for pseudorandom numbers

Input:
    sequence of n integers loaded from `input_file` (they will be mapped to numbers in range [0,1]).
    PRNG info from `input_file` must contain key `int_range` which is maximum possible value of generated numbers (doesn't have to occur)

Output:
    p-value of test

Sample usage: 
python scripts/z1_spacing_test.py --input-file 'results/mt_numbers_int.pkl'
"""
import numpy as np
import argparse
import pandas as pd
from scipy.stats import chi2
from z1_convert import ints_to_floats
from math import ceil

def ParseArguments():
    parser = argparse.ArgumentParser(description = "Spacing test")
    parser.add_argument('--input-file', default = "results/z1_XORG_numbers.pkl", required = False, help = 'Pickle file with generated numbers (default: %(default)s)')
    parser.add_argument('--alpha', default = "0", required = False, help = 'Beginning of interval (default: %(default)s)')
    parser.add_argument('--delta', default = "0.5", required = False, help = 'Width of interval (default: %(default)s)')
    
    args = parser.parse_args()
    return args.input_file, float(args.alpha), float(args.delta)

def get_spacings(floats: np.ndarray, a: float, b: float) -> list: # b > a
    """Calculate spacings for spacing test with numbering starting from 1 (C_1, ... C_k)"""
    Cs = [0]
    for i, x in enumerate(floats):
        if x >= a and x <= b:
            Cs.append(i+1 - Cs[-1]) # how big is step from last index  ind such that floats[ind] falls into [a,b]?

    return Cs[1:]

def get_bins_counts(Cs: list, s: int) -> np.ndarray:
    """Return counts of Cs in each of s+1 bins A_1, ... A_s""" # TODO jaki sens ma A_0? Było w skrypcie, ale nie ufam temu więc usunęłam
    bins = np.zeros((s,), dtype = np.uint8)
    for c in Cs:
        if c > s-1:
            bins[-1] += 1
        else:
            bins[c-1] += 1
    return bins

def spacing_test(numbers: np.ndarray, max_int: int, alpha: float, delta: float) -> float:
    """Run spacing test on numbers from 0 ... `max_int` with parameters `alpha`, `delta` and return computed p-value."""
    if alpha > 1 or alpha < 0:
        raise ValueError("Alpha ({alpha}) must be in range [0,1]")
    
    if delta <= 0 or delta > 0.5:
        raise ValueError(f"Delta = {delta} must be in (0,0.5)")
    beta = alpha + delta
    if beta < alpha or beta > 1: 
        raise ValueError(f"Wrong parameters: alpha + delta = {beta}")
    
    floats = ints_to_floats(numbers, max_int)
    
    # Step 1: Calculate spacings and choose number of bins s
    Cs = get_spacings(floats, alpha, alpha+delta)
    s = max(5, ceil(5*(1-delta)/delta)) if delta <= 0.5 else 5

    # Step 2: Find number of Cs in bins
    Os = get_bins_counts(Cs, s)

    # Step 3: Calculate chi_square statistic
    n = len(floats)                                           # TODO czy to na pewno ma być len(floats)?
    ps = np.full(shape = (s,), fill_value = (1-delta)*delta)
    ps[-1] = 1 - np.sum(ps[:-1])
    chi_sq = sum((Os - n*ps)**2/ n*ps)

    # Step 4: Calculate p-value of chi_sq statistic with s degrees of freedom; 
    # p_value = 1 - CDF(test_statistic)
    p_val = 1 - chi2.cdf(chi_sq, s)

    return p_val

def test_functions():
    fake_numbers = [0.1, 0.2, 0.1, 0.2, 0.4, 0.6, 0.1]
    assert get_spacings(fake_numbers, 0.3, 0.8) == [5,1]
    
    fake_Cs = [5,1,1,3,3,2,10,10,9,1,6,6,5,4,5,3,7,8]
    assert all(get_bins_counts(fake_Cs, 5) == np.array([3,1,3,1,10]))

if __name__ == '__main__':
    # Check if get_spacings and get_bins_counts work
    test_functions()

    # Read data and show information about tested numbers
    input_file, alpha, delta = ParseArguments()
    print(f'Reading numbers from {input_file}...')
    data = pd.read_pickle(input_file)
    numbers = data.pop('numbers') 
    print(f"Numbers info: {data}")
    print(f"First 5 numbers: {numbers[:5]}")
    max_int = data["max_int"]
    print(f"Numbers are from 0, ... {max_int}.\nRunning spacing test...\n")

    # Run test and show result
    result = spacing_test(numbers, max_int, alpha, delta)
    print(f'p-value: {result}')
