import numpy as np
import pandas as pd
import time

import argparse

import pickle
import platform

# Sample usage:
# python scripts_learn/sub_fib_gen.py --n 1000 --Mp 30 --k 100 --l 37 --seeds seeds.txt --output-file sub_fib_numbers.pkl --output_dir \D:\dokumenty

def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="100", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--Mp', default="30", required=False, help='power of 2 in parameter M (default: %(default)s)')
    parser.add_argument('--k', default="100", required=False, help='value of k parameter (default: %(default)s)')
    parser.add_argument('--l', default="37", required=False, help='value of l parameter (default: %(default)s)')
    parser.add_argument('--seeds', default="", required=False, help='name of the txt file with seeds (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    parser.add_argument('--output-dir', default="", required=False, help='output directory (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.Mp, args.k, args.l, args.seeds, args.output_file, args.output_dir


# funkcje

#LCG na potrzeby nie podania ziarna
def LCG(n):
    seed = int(time.time())
    a = 7 ** 5
    c = 0
    M = 2 ** 31
    result = [seed % M]
    for i in range(1, n):
        result.append((a * result[i-1] + c) % M)
    return result


#subtractive lagged fibbonaci generator
def sub_fib_gen(seed, gen=10, k=100, l=37, m=2**30):
    result = seed
    for i in range(len(seed)-1, len(seed) + gen, 1):
        result.append((result[i-k] - result[i-l]) % m)
    return result[-gen:]

# parametry z ParseArguments()

n, M, k, l, seed_name, output_file, output_dir = ParseArguments()

n = int(n)
M = 2 ** int(M)
k = int(k)
l= int(l)
segment_length = max(k,l) #liczba seedow potrzebna dla jednego pliku


seed = []
if (seed_name == ""):
    seed = LCG(max(k,l))
else:
    df_seeds = pd.read_csv(seed_name)
    seed = df_seeds["seeds"].tolist()
    if((len(seed) % max(l,k)) != 0 ):
        print("Podano niepoprawna liczbę seedów. Musi byc ona podzielna przez max(l,k)=" + str(max(l,k)))
        print("Brakuje " + str(max(l,k) - len(seed) % max(l,k)) + " seedow.")
        print("Brakujace seedy zostana uzupelnione za pomoca generatora LCG.")
        seed = seed + LCG(max(l,k) - (len(seed) % max(l,k)))


#generowanie

if(output_dir != ""):
    if(platform.system() == "Windows"):
        output_dir += "\\"
    else:
        output_dir += "/"

if(len(seed)==max(k,l)):
    sub_fib = sub_fib_gen(seed, n, k, l, M)

    # jesli output_file jest pusty, to wyswietl liczby, w przeciwnym przypadku zapisz je do pliku

    if output_file == "":
        print("Wygenerowane liczby: \n", sub_fib)
    else:

        data = {'PRNG': "sub_fib:  k=" + str(k) + ", l=" + str(l),
                'Modulus': M,
                'n': n,
                'seed': seed,
                'numbers': sub_fib}

        data_outfile = open(output_dir+output_file, 'wb+')
        pickle.dump(data, data_outfile)
        print("Wygenerowane liczby zapisano w: ", output_dir + output_file)

else:
    #przygtowywanie podstawy nazwy pliku
    output_file_string_list = output_file.split(".")
    base_name = "".join(output_file_string_list[:(len(output_file_string_list) - 1)])

    for i in range(0, len(seed) // max(k, l)):
        output_file_name = output_dir + base_name + str(i) + ".pkl"

        seed_segment = seed[(i * max(k, l)):((i+1) * max(k, l))]
        sub_fib = sub_fib_gen(seed_segment, n, k, l, M)
        data = {'PRNG': "sub_fib:  k=" + str(k) + ", l=" + str(l),
                'Modulus': M,
                'n': n,
                'seed': seed_segment,
                'numbers': sub_fib}

        data_outfile = open(output_file_name, 'wb+')
        pickle.dump(data, data_outfile)
        print("Zapisano plik: ", base_name + str(i) + ".pkl")
