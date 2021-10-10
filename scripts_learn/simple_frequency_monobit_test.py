import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.stats import norm

import argparse

import pickle
 
import pandas as pd
 
# Sample usage: 

# python  scripts_learn/simple_frequency_monobit_test.py --input-file results/lcg1_numbers.pkl 

def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    #parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file


input_file = ParseArguments()

numbers_info = pd.read_pickle(input_file)

prng_info = numbers_info['PRNG']

n=int(numbers_info['n'])

M= numbers_info['Modulus']

numbers = numbers_info['numbers']


# W tym przykladzie numbers to wektor liczb calkowitych z przedzialu 0,..,M-1,
# do TEGO TESTU musimy je zamienic na ciag bitow 0,1 i je zsumowac


Sn = 0

# UWAGA: liczba bitow bedzie inna niz n, trzebe je zliczac 

nr_of_bits = 0;

nr_digits = int(np.log2(M))


for nr in numbers: # petla po liczbach
    nr_binary_text = np.binary_repr(nr)    
    nr_of_bits = nr_of_bits + len(nr_binary_text)
 
    #zamiana nr_binary_text: a) na liste intow, b) zsumowanie ich
    # 2 *wektor01 -1 = wektor z +1 i -1
    wektor_min1_plus1 = 2*np.array(list(map(int, list(nr_binary_text))))-1
    
    # (nr_digits-len(nr_binary_text)) -- jak zapis jest mniej niz nr_digits cyfrowy to poprawka
    Sn = Sn + np.sum(wektor_min1_plus1) -(nr_digits-len(nr_binary_text))
    
n_final = int(np.log2(M) * n)

print("n = ", n, ",\t n_final = ", n_final)
print(" sum(2 x_i -1) = ", Sn)


Sn_final=Sn/np.sqrt(n_final)

print("Sn_final = ",Sn_final)
#liczymy p-wartosc: p = 2(1 − φ(|Sn |)
normal01 = norm()

p_value = 2*(1-normal01.cdf(np.abs(Sn_final)))

print("FREQUENCY MONOBIT TEST result:")
print("p-wartosc = ", np.round(p_value,5))



 
