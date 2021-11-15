import time
import argparse
import pickle


def ParseArguments():
    parser = argparse.ArgumentParser(description="QCG II PRNG")
    parser.add_argument('-n', default="100", required=False, help='number of generated numbers (default: %(default)s)')
    parser.add_argument('-a', default="2", required=False, help='parameter \'a\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('-b', default="3", required=False, help='parameter \'b\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('-c', default="1", required=False, help='parameter \'c\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('-M', required=False, help='Modulus \'M\' in PRNG recursion (default: 2^512)')
    parser.add_argument('--seed', required=False, help='seed in PRNG recursion')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.a, args.b, args.c, args.M, args.seed, args.output_file

def QCG_II_Gen(n, seed, M = 2**512, a = 2, b = 3, c = 1):
    numbers = [0] * n
    numbers[0] = seed % M
    for i in range(1,n):
        numbers[i] = (a*numbers[i-1]**2 + b*numbers[i-1] + c) % M

    return numbers


n, a, b, c, M, s, output_file = ParseArguments()

n = int(n)
a = int(a)
b = int(b)
c = int(c)
if M:
    M = int(M)
else: M = 2**512
if s:
    s = int(s)
else: s = int(time.time())

numbers = QCG_II_Gen(n, s, M, a, b, c)

if output_file==" ": #jeżeli nie podamy pliku to wypisz liczby w konsoli
    print("Wygenerowane liczby: \n", numbers)
else:
    data = {'PRNG': "QCG II: a="+str(a)+", b="+str(b)+", c="+str(c),
            'Modulus' : M,
            'n' : n,
            'numbers': numbers}
    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)