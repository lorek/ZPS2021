import argparse
import pandas as pd
from z1_convert import ints_to_floats
from scipy.stats import kstest
from time import perf_counter as time

def ParseArguments():
    parser = argparse.ArgumentParser(description = "Spacing test")
    parser.add_argument(
        '--input-file', default = "results/z1_XORG_numbers_int.pkl", required = False, 
        help = 'Pickle file with generated numbers (default: %(default)s)'
        )
    
    args = parser.parse_args()
    return args.input_file

if __name__ == '__main__':
    # Read data and show information about tested numbers
    input_file = ParseArguments()
    print(f'Reading numbers from {input_file}...')
    data = pd.read_pickle(input_file)
    numbers = data.pop('numbers') 
    print(f"Numbers info: {data}")
    print(f"First 5 numbers: {numbers[:5]}")
    max_int = data["max_int"]
    print(f"Numbers are from 0, ... {max_int}.\nRunning KS test...\n")

    # Numbers must be converted to U(0,1)
    floats = ints_to_floats(numbers, max_int)

    # Run test and show result
    start = time()
    stat, pval = kstest( numbers, cdf = 'uniform')
    time = time() - start
    print(f'p-value: {pval} (value of KS statistic = {stat})')
    print(f'running time: {time:.3}s')






    
