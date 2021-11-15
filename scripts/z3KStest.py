import numpy as np
import scipy.stats as sts
import argparse
import pandas as pd

def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorov–Smirnov test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='input file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file

input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

n = int(numbers_info['n']) #ilość liczb 
M = int(numbers_info['Modulus']) #Modlulo
numbers = numbers_info['numbers'] #liczby (pseudolosowe)

numbers = list(map(lambda x: x/M, numbers)) #zamiana na liczby z przedziału (0 , 1)

test = sts.kstest(numbers, cdf = 'uniform')

#WNIOSKI
print("Kolmogorov–Smirnov test results:")
print("p-value: "+str(test[1]))
print("Statistic: "+str(test[0]))
print("PARAMETERS:")
print("M: "+str(numbers_info['Modulus']))
print("n: "+str(numbers_info['n']))
print("Numbers have beed generated with: "+str(numbers_info['PRNG']))
