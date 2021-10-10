import numpy as np
import matplotlib.pyplot as plt
import time

import argparse

import pickle
 
# Sample usage: 
# python scripts_learn/simple_lcg_prng.py --n 1000 --output-file results/lcg1_numbers.pkl

def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.output_file


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

n, output_file = ParseArguments()

n = int(n)

# inne parametry, recznie

s = int(time.time())

M = 2**10
a = 3
c = 7

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
    
