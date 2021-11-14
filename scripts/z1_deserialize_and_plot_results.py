# This code can be used to deserialize numbers stored in pickle and show histogram of them.
# Numbers are loaded from input-file, deserialized and written to output-file.

import matplotlib.pyplot as plt
import argparse
import pandas as pd
from time import perf_counter as time

def ParseArguments():
    parser = argparse.ArgumentParser(description="Load generated numbers from pickle")
    parser.add_argument('--input-file', default = 'results/z1_XORG_numbers.pkl', required = False, help = 'File with numbers stored as pickle (default: %(default)s)')
    parser.add_argument('--output-file', default = 'deserialized_numbers.txt', required = False, help = 'Output file (default: %(default)s)')
    parser.add_argument('--bins', required = False, help = 'Number of bins in histogram (default: %(default)s)')
    
    args = parser.parse_args()
    return args.input_file, args.output_file, args.bins

def deserialize(input_file):
    print(f'Reading numbers from {input_file}...')
    data = pd.read_pickle(input_file)
    return data['numbers']

if __name__ == '__main__':
    input_file, output_file, bins = ParseArguments()
    start = time()
    
    numbers = deserialize(input_file)
    with open(output_file, 'w') as f:
        f.write(str(numbers))

    time = time() - start
    n = len(numbers)
    print(f'({round(time, 3)}s) Deserialized numbers (n = {n}) can be found in {output_file}.')

    nbins = 256 if not bins else int(bins)
    plt.hist(numbers, ec = 'black', bins = nbins)
    plt.title(f"Histogram of {n} numbers loaded from {input_file} ({nbins} bins)")
    plt.show()



    
    

