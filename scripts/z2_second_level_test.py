import pandas as pd
import numpy as np
from scipy.stats import chisquare
import argparse
from scipy.stats.distributions import chi2

def ParseArguments():
    parser = argparse.ArgumentParser(description="Second level testing")
    parser.add_argument('--input-file', default="p-values.csv", required=False, help='input file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()

p_values = pd.read_csv(input_file)
p_values = p_values["p-value"].to_list()


observed_bins = [0] * 10
for p_value in p_values:
    for i in range(10):
        if (i/10 <= p_value) & (p_value <= (i+1)/10):
            observed_bins[i] += 1

n = len(p_values)
expected_bins = [n/10] * 10


test_statistic = sum([(m-n)**2 / n for m,n in zip(observed_bins,expected_bins)])
P_value = chi2.sf(test_statistic,9)
print(P_value)