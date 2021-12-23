import time
import argparse
import pickle
import pandas as pd
import numpy as np


def ParseArguments():
    parser = argparse.ArgumentParser(description="QCG II PRNG")
    parser.add_argument('-n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('-a', default="2", required=False, help='parameter \'a\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('-b', default="3", required=False, help='parameter \'b\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('-c', default="1", required=False, help='parameter \'c\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('-M', required=False, help='Modulus \'M\' in PRNG recursion (default: 2^32)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="seeds.csv", required=False, help='File (.csv) with seeds (default: %(default)s)')
    parser.add_argument('--output-dir', default="pickles_dir", required=False, help='Directory to save .pkl files generated with seeds (default: %(default)s)')
    
    args = parser.parse_args()

    return args.n, args.a, args.b, args.c, args.M, args.output_file, args.seeds, args.output_dir

def QCG_II_Gen(n, seed, M = 2**32, a = 2, b = 3, c = 1):
    numbers = [0] * n
    numbers[0] = seed % M
    for i in range(1,n):
        numbers[i] = (a*numbers[i-1]**2 + b*numbers[i-1] + c) % M

    return numbers


n, a, b, c, M, output_file, seeds_file, output_dir = ParseArguments()

if(seeds_file!=""):
	df_seeds=pd.read_csv(seeds_file)
	seeds=df_seeds["seeds"].to_numpy()
else:
	seeds  = np.array([int(time.time())])

n = int(n)
a = int(a)
b = int(b)
c = int(c)
if M:
    M = int(M)
else: M = 2**32

if(output_dir!=""):
	output_dir +="/"

if len(seeds)==1:
	qcg2 = QCG_II_Gen(n, seeds[0], M, a, b, c)

	if output_file=="":
		print("Wygenerowane liczby: \n",qcg2)
	else:
		data = {'PRNG': "QCG II: a="+str(a)+", b="+str(b)+", c="+str(c),
            'Modulus' : M,
            'n' : n,
            'numbers': qcg2}
					
		data_outfile = open(output_file, 'wb+')
		pickle.dump(data, data_outfile)
		print("Wygenerowane liczby zapisano w: ", output_file)
		
else: # jest wiecej seedow	
	output_file_list = output_file.split(".")
	output_file_prefix = "".join(output_file_list[:(len(output_file_list)-1)])

	for nr, seed in enumerate(seeds):
		qcg2 = QCG_II_Gen(n, seed, M, a, b, c)
		
		output_file = output_dir+output_file_prefix+"_seed_"+str(nr)+".pkl"
		
		data = {'PRNG': "QCG II: a="+str(a)+", b="+str(b)+", c="+str(c),
                'Modulus' : M,
                'n' : n,
                'numbers': qcg2}
		 
		data_outfile = open(output_file, 'wb+')
		pickle.dump(data, data_outfile)
		
		print("Saving file nr ",nr,",\t",output_file)