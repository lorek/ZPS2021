import numpy as np
import argparse
import pickle

def ParseArguments():
    parser = argparse.ArgumentParser(description="MT19937 PRNG")
    parser.add_argument('-n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('-M', required=False, help='Modulus \'M\' in PRNG (default: 2^64)')
    parser.add_argument('--seed', required=False, help='seed in PRNG')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.M, args.seed, args.output_file

n, M, s, output_file = ParseArguments()

n = int(n)
if M:
    M = int(M)
else: M = 2**64
if s:
    PRNG = np.random.Generator(np.random.MT19937(int(s)))
else: PRNG = np.random.Generator(np.random.MT19937())

numbers = PRNG.integers(low = 0, high = M - 1, size = n, dtype = np.uint64)

if output_file==" ": #jeżeli nie podamy pliku to wypisz liczby w konsoli
    print("Wygenerowane liczby: \n", numbers)
else:
    data = {'PRNG': "MT19937",
            'Modulus' : M,
            'n' : n,
            'numbers': numbers}
    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)
