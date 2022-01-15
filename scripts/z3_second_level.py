import argparse 
import pandas as pd
import numpy as np
from scipy.stats.distributions import chi2


def ParseArguments():
    parser = argparse.ArgumentParser(description="Second Level Test")
    parser.add_argument('--input-file', default="p-values.csv", required=False, help='input file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()

df_p_values = pd.read_csv(input_file)
p_values = df_p_values["p-value"].to_numpy()
bin = np.array([0]*10)
n = len(p_values)

for value in p_values:
    for i in range(0,10):
        if i/10 <= value < (i+1)/10:
            bin[i] += 1
            break

test_stat = sum((bin - n/10)**2/(n/10))
final_p_value = chi2.sf(test_stat,9)
print("Final p-value:", final_p_value)


