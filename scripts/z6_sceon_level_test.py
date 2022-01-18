import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import argparse
import pickle
import glob, os
import pandas as pd
from scipy.stats import chisquare


def second_level_test(pvalues):
    bins =[0]*10
    n= len(pvalues)
    print(n)

    for i in range(0, 10):
        bins[i] = sum((int((i/10)<= p and p<(i+1)/10 )for p in pvalues))
    bins[-1]+= sum((int(p==1)for p in pvalues))
    print(sum(bins))
    print((bins))
    exp = [n/10]*10
    print((exp))
    print(sum(exp))
    pv = chisquare(f_obs=bins, f_exp=exp)[1]
    print(pv)
    return 1

def ParseArguments():
    parser = argparse.ArgumentParser(description="Second Level Test")
    parser.add_argument('--input-file', default="pvpcg64runs.csv", required=False, help='input file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file
input_file = ParseArguments()

dane = pd.read_csv(input_file)
p_values = dane['p-value'].to_list()
'''
p_values = []

with pd.read_csv(input_file, chunksize=10) as reader:
    for chunk in reader:
        p_values+=list(chunk["p-value"])
        #p_values = np.append(p_values, list(chunk["p-value"]))
'''

print(p_values[:5])
print(second_level_test(p_values))
