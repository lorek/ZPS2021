import numpy as np
import argparse
import pickle
import pandas as pd

def ParseArguments():
    parser = argparse.ArgumentParser(description="MT19937 PRNG")
    parser.add_argument('-n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('-M', required=False, help='modulus \'M\' in PRNG (default: 2^64)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--seeds', default="seeds.csv", required=False, help='file (.csv) with seeds  (default: %(default)s)')
    parser.add_argument('--output-dir', default="pickles_dir", required=False, help='directory to save .pkl files generated with seeds (default: %(default)s)')
    
    args = parser.parse_args()

    return args.n, args.M, args.output_file, args.seeds, args.output_dir

n, M, output_file, seeds_file, output_dir = ParseArguments()

n = int(n)
if M:
    M = int(M)
else: M = 2**64

if(seeds_file!=""):
    df_seeds=pd.read_csv(seeds_file)
    seeds=df_seeds["seeds"].to_numpy()
    PRNG = np.random.Generator(np.random.MT19937(seeds[0]))
else:
    PRNG = np.random.Generator(np.random.MT19937())
    seeds = [0]

if(output_dir!=""):
	output_dir +="/"

if len(seeds)==1:
	numbers = PRNG.integers(low = 0, high = M - 1, size = n, dtype = np.uint64)

	if output_file=="":
		print("Wygenerowane liczby: \n",numbers)
	else:
		data = {'PRNG': "MT19937",
            'Modulus' : M,
            'n' : n,
            'numbers': numbers}				
		data_outfile = open(output_file, 'wb+')
		pickle.dump(data, data_outfile)
		print("Wygenerowane liczby zapisano w: ", output_file)
		
else: # jest wiecej seedow	
    output_file_list = output_file.split(".")
    output_file_prefix = "".join(output_file_list[:(len(output_file_list)-1)])

    for nr, seed in enumerate(seeds):
        PRNG = np.random.Generator(np.random.MT19937(seed))
        numbers = PRNG.integers(low = 0, high = M - 1, size = n, dtype = np.uint64)
        output_file = output_dir+output_file_prefix+"_seed_"+str(nr)+".pkl"
        data = {'PRNG': "MT19937",
            'Modulus' : M,
            'n' : n,
            'numbers': numbers}

        data_outfile = open(output_file, 'wb+')
        pickle.dump(data, data_outfile)    
        print("Saving file nr ",nr,",\t",output_file)
