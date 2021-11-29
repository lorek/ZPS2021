import numpy as np
from scipy.stats import norm
import argparse
import pandas as pd

def ParseArguments():
    parser = argparse.ArgumentParser(description="Cumulative Sums Test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='input file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file

input_file = ParseArguments()
numbers_info = pd.read_pickle(input_file)

n = int(numbers_info['n']) #ilość liczb 
M = int(numbers_info['Modulus'])
numbers_length = (M-1).bit_length() #długość liczb binarnie
numbers = numbers_info['numbers'] #liczby (pseudolosowe)
binary_numbers = list()
for i in range(0, n):
    binary_numbers = binary_numbers + list([0] * (numbers_length - len(bin(numbers[i])) + 2)) + list(bin(numbers[i]))[2:] #zamiana liczb na postać binarną i ustawienie ich w ciąg

partial_sums = [0] * len(binary_numbers)
binary_numbers = list(map(lambda x: (int(2*int(x)-1)), binary_numbers)) #zamiana 0 -> -1 i 1 -> 1 w ciągu binarnym
partial_sums[0] = binary_numbers[0]

for i in range(1, len(binary_numbers)):
    partial_sums[i]  =  binary_numbers[i]+partial_sums[i-1] #liczenie sum częściowych dla ciągu -1, 1

partial_sums = list(map(abs, partial_sums)) #wartość bezwzględna z każdej sumy częściowej

z = max(partial_sums) # maksimum modułu sum częściowych
N = len(binary_numbers) #długość ciągu binarnego

first_sum_seq1 = [0]
first_sum_seq2 = [0]
second_sum_seq1 = [0]
second_sum_seq2 = [0]

for i in range(int(np.floor((-N/z + 1)/4)), int(np.ceil((N/z - 1)/4))): #liczenie składowych p-wartości
    first_sum_seq1.append(norm.cdf((4*i + 1)*z/np.sqrt(N)))
    first_sum_seq2.append(norm.cdf((4*i - 1)*z/np.sqrt(N)))

for i in range(int(np.floor((-N/z - 3)/4)), int(np.ceil((N/z - 1)/4))):
    second_sum_seq1.append(norm.cdf((4*i + 3)*z/np.sqrt(N)))
    second_sum_seq2.append(norm.cdf((4*i + 1)*z/np.sqrt(N)))

p_value = 1 + sum(first_sum_seq2) + sum(second_sum_seq1)  - sum(second_sum_seq2)  - sum(first_sum_seq1) #p-wartość
#WNIOSKI
print("CUMULATIVE SUMS TEST results:")
print("p-value: "+str(p_value))
print("If p-value is greater than 0.01, we can conclude that we have generated random numbers. Otherwise we have non-random numbers.")
print("PARAMETERS:")
print("M: "+str(numbers_info['Modulus']))
print("n: "+str(numbers_info['n']))
print("Numbers have been generated with: "+str(numbers_info['PRNG']))