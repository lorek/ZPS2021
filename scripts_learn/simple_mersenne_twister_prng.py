import numpy as np
import matplotlib.pyplot as plt
import time

import argparse

import pickle
 
# using built-in MT19937 

# Sample usage: 
# python scripts_learn/simple_mersenne_twister_prng.py --n 1000 --form float --output-file results/mt_numbers_float.pkl
# python scripts_learn/simple_mersenne_twister_prng.py --n 1000 --form int --output-file results/mt_numbers_int.pkl



def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--form', default="int", required=False, help='format: int, float (default: %(default)s)')
    
    args = parser.parse_args()

    return args.n, args.output_file, args.form

n, output_file, form = ParseArguments()

n = int(n)

from numpy.random import MT19937 

s = int(time.time())

rng_mt19937 = np.random.default_rng(np.random.MT19937(seed=s))

numbers_mt19937 = rng_mt19937.random(n)
 

if output_file=="":
    print("Wygenerowane liczby: \n",lcg1)
else:
    if(form=="float"):
        data = {'PRNG': "MT19937",
            'n' : n,
            'numbers': numbers_mt19937}
                
        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
    
    if(form=="int"):
        numbers_mt19937=numbers_mt19937*2**32
        numbers_mt19937=numbers_mt19937.astype(int)
        
        data = {'PRNG': "MT19937",
            'n' : n,
            'Modulus': 2**32,
            'numbers': numbers_mt19937}
                
        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)
        
    print("Wygenerowane liczby zapisano w: ", output_file,", format: ", form)
    
