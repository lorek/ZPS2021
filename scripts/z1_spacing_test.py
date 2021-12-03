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
from time import perf_counter as time

def ParseArguments():
    parser = argparse.ArgumentParser(description = "Spacing test")
    parser.add_argument('--input-file', default = "results/z1_XORG_numbers_int.pkl", required = False, help = 'Pickle file with generated numbers (default: %(default)s)')
    parser.add_argument('--output-file', default = "test_results/spacing_XORG.txt", required = False, help = 'Where results will be stored? If not provided, results are not saved. (default: %(default)s)')
    parser.add_argument('--alpha', default = "0", required = False, help = 'Beginning of interval (default: %(default)s)')
    parser.add_argument('--delta', default = "0.5", required = False, help = 'Width of interval (default: %(default)s)')
    
    args = parser.parse_args()
    return args.input_file, args.output_file, float(args.alpha), float(args.delta)

def get_spacings(floats: np.ndarray, a: float, b: float) -> list: # b > a
    """Calculate spacings for spacing test with numbering starting from 1 (C_1, ... C_k)"""
    Cs = []
    space = 0
    for x in floats:
        if x >= a and x <= b:
            Cs.append(space)
            space = 0
        else:
            space += 1

    return Cs

def get_bins_counts(Cs: list, s: int) -> np.ndarray:
    """Return counts of Cs in each of s+1 bins A_0, ... A_s"""
    bins = np.zeros((s+1,), dtype = np.uint8)
    for c in Cs:
        if c > s-1:
            bins[-1] += 1
        else:
            bins[c] += 1
    return bins

def spacing_test(numbers: np.ndarray, max_int: int, alpha: float, delta: float) -> float:
    """Run spacing test on numbers from 0 ... `max_int` with parameters `alpha`, `delta` and return computed p-value."""
    # Setup: read params and convert numbers
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

    # Step 3: Calculate ps array
    ps = np.apply_along_axis(lambda i: 0.5*(1 - 0.5)**i, 0, np.array(range(s+1))) # fill values for i = 0, ... s
    ps[-1] = 1 - sum(ps[:-1])                                                     # correct the last term so that all sum up to 1
    assert (sum(ps) == 1)
    
    # Step 4: Calculate chi_square statistic
    k = len(Cs)
    chi_sq = sum((Os - k*ps)**2/ k*ps)

    # Step 4: Calculate p-value of chi_sq statistic with s degrees of freedom; 
    # p_value = 1 - CDF(test_statistic)
    p_val = 1 - chi2.cdf(chi_sq, s)

    return p_val

def test_functions():
    fake_numbers = [0.4, 0.1, 0.2, 0.3, 0.4, 0.1, 0.5]
    spacings = get_spacings(fake_numbers, 0.3, 0.8)
    assert spacings == [0,2,0,1]
    
    fake_Cs = [0,0,1,2,5,0,1,3,4,6,8,0,2,3]
    assert all(get_bins_counts(fake_Cs, 5) == np.array([4,2,2,2,1,3]))

if __name__ == '__main__':
    # Check if get_spacings and get_bins_counts work
    test_functions()

    # Read data and show information about tested numbers
    input_file, output_file, alpha, delta = ParseArguments()
    print(f'Reading numbers from {input_file}...')
    data = pd.read_pickle(input_file)
    numbers = data.pop('numbers') 
    print(f"Numbers info: {data}")
    print(f"First 5 numbers: {numbers[:5]}")
    max_int = data["max_int"]
    print(f"Numbers are from 0, ... {max_int}.\nRunning spacing test...\n")

    # Run test and show result
    start = time()
    result = spacing_test(numbers, max_int, alpha, delta)
    time = time() - start

    summary = {
        "test": "spacing",
        "input_file": input_file,
        "alpha": alpha,
        "delta": delta,
        "p-value": result
    }
    print(f'p-value: {result}')
    print(f'running time: {time:.3}s')

    # Save summary
    if (output_file):
        out = open(output_file, "w")
        out.write(str(summary))
        print(f"\nSummary of test can be found in {output_file}.")
        out.close()
