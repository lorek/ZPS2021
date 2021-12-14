import numpy as np
from numpy.lib.function_base import append
from scipy.stats import norm
import argparse
import pandas as pd
import glob

def Cusum(n, numbers_length, numbers):
    binary_numbers = list()
    for i in range(0, n):
        for _ in range(numbers_length - len(bin(numbers[i])) + 2):
            binary_numbers.append(0)
        for val in list(bin(numbers[i]))[2:]:
            binary_numbers.append(val)

    partial_sums = [0] * len(binary_numbers)
    binary_numbers = list(map(lambda x: (int(2*int(x)-1)), binary_numbers)) #zamiana 0 -> -1 i 1 -> 1 w ciągu binarnym
    partial_sums[0] = binary_numbers[0]

    for i in range(1, len(binary_numbers)):
        partial_sums[i]  =  binary_numbers[i]+partial_sums[i-1] #liczenie sum częściowych dla ciągu -1, 1

    partial_sums = list(map(abs, partial_sums)) #wartość bezwzględna z każdej sumy częściowej

    z = max(partial_sums) # maksimum modułu sum częściowych
    N = len(binary_numbers) #długość ciągu binarnego

    first_sum_seq1 = 0
    first_sum_seq2 = 0
    second_sum_seq1 = 0
    second_sum_seq2 = 0

    Nsqrt = np.sqrt(N)

    for i in range(int(np.floor((-N/z + 1)/4)), int(np.ceil((N/z - 1)/4))): #liczenie składowych p-wartości
        first_sum_seq1 += (norm.cdf((4*i + 1)*z/Nsqrt))
        first_sum_seq2 += (norm.cdf((4*i - 1)*z/Nsqrt))

    for i in range(int(np.floor((-N/z - 3)/4)), int(np.ceil((N/z - 1)/4))):
        second_sum_seq1 += (norm.cdf((4*i + 3)*z/Nsqrt))
        second_sum_seq2 += (norm.cdf((4*i + 1)*z/Nsqrt))

    p_value = 1 + first_sum_seq2 + second_sum_seq1  - second_sum_seq2  - first_sum_seq1 #p-wartość
    return(p_value)


def ParseArguments():
    parser = argparse.ArgumentParser(description="Cumulative Sums Test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='input file (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False, help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False, help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file



input_file, input_dir, pval_file = ParseArguments()

if input_dir=="":
    numbers_info = pd.read_pickle(input_file)
    n = int(numbers_info['n']) #ilość liczb 
    M = int(numbers_info['Modulus'])
    numbers_length = (M-1).bit_length() #długość liczb binarnie
    numbers = numbers_info['numbers'] #liczby (pseudolosowe)
    p_value = Cusum(n, numbers_length, numbers) #p-wartość

    print("CUMULATIVE SUMS TEST results:")
    print("p-value: "+str(p_value))
    print("If p-value is greater than 0.01, we can conclude that we have generated random numbers. Otherwise we have non-random numbers.")
    print("PARAMETERS:")
    print("M: "+str(numbers_info['Modulus']))
    print("n: "+str(numbers_info['n']))
    print("Numbers have been generated with: "+str(numbers_info['PRNG']))
    pvals = []
    pvals.append(p_value)
    print("Saving p-value to ",pval_file)
    df=pd.DataFrame(pvals,columns=["p-value"])
    df.to_csv(pval_file, index = False)
else:
    print("input_dir = ", input_dir)
    pvals = []
    file_list = list((glob.glob(input_dir + "/**.pkl")))
    file_list.sort()
    for file_name in file_list:
        print("Processing file ", file_name, " ...")
        numbers_info = pd.read_pickle(file_name)
        n=int(numbers_info['n'])
        M= numbers_info['Modulus']
        numbers = numbers_info['numbers']
        numbers_length = (M-1).bit_length()
        pval = Cusum(n, numbers_length, numbers)
        pvals.append(pval)

    print("Saving p-values to ",pval_file)
    df=pd.DataFrame(pvals,columns=["p-value"])
    df.to_csv(pval_file, index = False)