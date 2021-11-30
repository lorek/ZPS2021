import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.stats import norm

import argparse

import pickle
 
import glob, os
 
import pandas as pd
 
# Sample usage: 
# one .pkl
# python  scripts_learn/simple_frequency_monobit_test_many_seeds.py --input-file results_sample/lcg1_numbers_seed_0.pkl --pval-file results_sample/pvals.csv
# 
# many .pkl files
# python   scripts_learn/simple_frequency_monobit_test_many_seeds.py --input-file results_sample/lcg1_numbers_seed_0.pkl --input-dir results_sample/ --pval-file results_sample/p-values.csv

 
def freq_mon_test(numbers, M,n):

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

	#print("n = ", n, ",\t n_final = ", n_final)
	#print(" sum(2 x_i -1) = ", Sn)


	Sn_final=Sn/np.sqrt(n_final)

	#print("Sn_final = ",Sn_final)
	#liczymy p-wartosc: p = 2(1 − φ(|Sn |)
	normal01 = norm()

	p_value = 2*(1-normal01.cdf(np.abs(Sn_final)))
	
	return p_value 


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    #parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='input .pkl file (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False, help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False, help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file,args.input_dir, args.pval_file


input_file, input_dir, pval_file = ParseArguments()


# IDEA: jesli input_dir pusty, to po prostu jeden test na pliku input_file  i 1 p-wart. zapisujemy do pval_file
# jesli input_dir != "", to test dla kazdego .pkl z tego katalogu i p-wart. zapisujemy w kolejnych linijkach pval_file


if input_dir=="": # one .pkl file

	numbers_info = pd.read_pickle(input_file)

	prng_info = numbers_info['PRNG']

	n=int(numbers_info['n'])

	M= numbers_info['Modulus']

	numbers = numbers_info['numbers']

	pval = freq_mon_test(numbers,M,n)

	print("pval = ", np.round(pval ,5))
	pvals = []
	pvals.append(pval)
	print("Saving p-value to ",pval_file)
	df=pd.DataFrame(pvals,columns=["p-value"])
	df.to_csv(pval_file)
	
else: # many .pkl files
	print("input_dir = ", input_dir)
	pvals = []
	file_list = list((glob.glob(input_dir + "/**.pkl")))
	file_list.sort()
	for file_name in file_list:
		print("Processing file ", file_name, " ...")
		numbers_info = pd.read_pickle(file_name)
		
		prng_info = numbers_info['PRNG']
		n=int(numbers_info['n'])
		M= numbers_info['Modulus']
		numbers = numbers_info['numbers']
		pval = freq_mon_test(numbers,M,n)
		pvals.append(pval)
		
	print("Saving p-values to ",pval_file)
	df=pd.DataFrame(pvals,columns=["p-value"])
	df.to_csv(pval_file, index = False)
		
	 
 


 
