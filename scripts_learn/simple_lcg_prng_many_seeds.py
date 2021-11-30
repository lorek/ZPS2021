import numpy as np
import matplotlib.pyplot as plt
import time

import pandas as pd

import argparse

import pickle
 
# Sample usage: 
# python  scripts_learn/simple_lcg_prng_many_seeds.py --seeds scripts_learn/sample_seeds.csv --output-file my_gen_numbers.pkl --output-dir results_sample/

def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="", required=False, help='File (.csv) with seeds  (default: %(default)s)')
    parser.add_argument('--output-dir', default="", required=False, help='File (.csv) with seeds  (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.output_file, args.seeds, args.output_dir


# funkcje 

# naiwna implementacja lcg (moze miec problemy z duzym n)
# (jak powinno byc -- zob. https://en.wikipedia.org/wiki/Linear_congruential_generator)

def LCG(n, seed, Modulus, a, c):
    # wektor dlugosci n, typu int
    lcg = np.zeros(n, dtype='int')
    lcg[0] = seed % Modulus
    for i in range(1,n):
        lcg[i]= (a * lcg[i-1] + c) % Modulus

    return lcg 
              

# parametry z ParseArguments()

n, output_file, seeds_file, output_dir = ParseArguments()

n = int(n)

if(seeds_file!=""):
	print("ASDF")
	df_seeds=pd.read_csv(seeds_file)
	seeds=df_seeds["seeds"].to_numpy()
else:
	seeds  = np.array([int(time.time())])
 

# inne parametry, recznie



M = 2**10
a = 3
c = 7


# jesli seeds jest rozmiaru 1, to zapisujemy do pliku output_file jeden ciag
# w przeciwnym przypadku to output_dir zapisujemy tyle plikow ile jest seedow

	
if(output_dir!=""):
	output_dir +="/";
	
		
if len(seeds)==1:
	lcg1 = LCG(n, s, M, a, c)
 
	# jesli output_file jest pusty, to wyswietl liczby, w p.p. zapisz je do pliku

	if output_file=="":
		print("Wygenerowane liczby: \n",lcg1)
	else:
		# tak dla .csv, ale bedziemy uzywali pickle()
		#np.savetxt(output_file,lcg1,delimiter=";") 
		
		data = {'PRNG': "LCG:  a="+str(a)+", c="+str(c),
				'Modulus' : M,
				'n' : n,
				'numbers': lcg1}
					
		data_outfile = open(output_file, 'wb+')
		pickle.dump(data, data_outfile)
		print("Wygenerowane liczby zapisano w: ", output_file)
		
else: # jest wiecej seedow	
	# przygotujmy nazwe -- zostawiamy tekst przed ostatnia kropka (np. z "asdf.asf_afs.pkl" zostawi "asdfasf_afs")
	output_file_list = output_file.split(".")
	output_file_prefix = "".join(output_file_list[:(len(output_file_list)-1)])

		
	for nr, seed in enumerate(seeds):
		lcg1 = LCG(n, seed, M, a, c)
		
		output_file = output_dir +output_file_prefix+"_seed_"+str(nr) + ".pkl"
		
		data = {'PRNG': "LCG:  a="+str(a)+", c="+str(c),
				'Modulus' : M,
				'n' : n,
				'numbers': lcg1}
		 
		data_outfile = open(output_file, 'wb+')
		pickle.dump(data, data_outfile)
		
		print("Saving file nr ",nr,",\t",output_file)
		
		
    
