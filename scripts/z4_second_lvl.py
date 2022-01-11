import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
import argparse


def ParseArguments():
    parser = argparse.ArgumentParser(description="Second level testing")
    parser.add_argument('--input-file', default="p-values.csv", required=False,
                        help='input .csv file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()


def to_bins(pvals_list):
    my_bins = [i / 10 for i in range(11)]
    res = np.histogram(pvals_list, bins=my_bins)
    return list(res[0])


data = pd.read_csv(input_file)
pv = data['p-value'].to_list()
n = len(pv)

pval_bins = np.array(to_bins(pv))

expected = np.array([n / 10] * 10)
p_value = chisquare(pval_bins, expected)[1]

print(p_value)
print("Random?:", p_value >= 0.0001)
