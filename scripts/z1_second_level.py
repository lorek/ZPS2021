"""
This script runs second-level test using Kolmogorov–Smirnov uniformity test on p-values stored in `input-file`.
`input-file` should be csv with one column named "p-value".

Result (single p-value) is saved in `output-file`.

Sample usage: 
python scripts/z1_second_level.py --input-file 'results/spacing_XORG_pvalues.csv' --output-file 'results/spacing_XORG_second_level_result.txt'
"""

from scipy.stats import kstest
import argparse
import pandas as pd
from time import perf_counter as time

def ParseArguments():
    parser = argparse.ArgumentParser(description = "Second-level testing")
    parser.add_argument('--input-file', default = "results/spacing_XORG_pvalues.csv", required = False, help = 'Csv file with p-values (default: %(default)s)')
    parser.add_argument('--output-file', default = "results/spacing_XORG_second_level_result.txt", required = False, help = 'Where results will be stored? (default: %(default)s)')
    
    args = parser.parse_args()
    return args.input_file, args.output_file

if __name__ == "__main__":
    input_file, output_file = ParseArguments()
    pvalues = pd.read_csv(input_file)["p-value"].to_numpy()
    print(f"Running KS-test on pvalues list:\n{pvalues}\n...")
    start = time()
    stat, pval = kstest(pvalues, cdf = 'uniform')
    time = time() - start
    print(f'p-value: {pval} (value of KS statistic = {stat})')
    print(f'running time: {time:.3}s')
    with open(output_file, "w") as f:
        f.write(str(pval))
    print(f"Obtained p-value is saved in {output_file}.")

    