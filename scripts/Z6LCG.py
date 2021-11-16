import random
import time
import argparse
import pickle

def ParseArguments():
    parser = argparse.ArgumentParser(description="LCG")
    parser.add_argument('--n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('--X0', required=False,
                        help='seed in PRNG recursion')
    parser.add_argument('--a', default="1664525", required=False,
                        help='parameter \'a\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--b', default="1013904223", required=False,
                        help='parameter \'b\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--M', required=False, help='Modulus \'M\' in PRNG recursion (default: 2^32)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.X0, args.a, args.b, args.M, args.output_file

def LCG(n, X0=random.randint(0, 2 ** 32 - 1), a=1664525, b=1013904223, M=2 ** 32):
    randoms = []
    X0 = X0 % M
    randoms.append((a * X0 + b) % M)
    for i in range(n):
        randoms.append((a * randoms[i] + b) % M)
    return randoms
"""
zał. generatora:
X0: 0<=X0<M
M: M>0
a: 0<=a<M
b: 0<=b<M
W generattorze LCG ziarnem jest pierwszy wyraz - X0
za kazdym razem X0 jest losowane za pomoca funkcji random.randint()
"""
n, X0, a, b, M, output_file = ParseArguments()

n = int(n)
if X0:
    X0 = int(X0)
else: X0 = int(time.time())
a = int(a)
b = int(b)
if M:
    M = int(M)
else: M = 2 ** 32

randoms = LCG(n, X0, a, b, M)

if output_file=="":
    print("Wygenerowane liczby: \n", randoms)
else:
    data = {'PRNG': "LCG: a="+str(a)+", b="+str(b),
            'Modulus' : M,
            'n' : n,
            'numbers': randoms}
    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)


#if __name__ == '__main__':
#   print(LCG(2))
