import argparse
import pickle
import sympy
import random


def ParseArguments():
    parser = argparse.ArgumentParser(description="BBSG PRNG")
    parser.add_argument('--n', default="1000", required=False,
                        help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--x', default=str(30**10), required=False,
                        help='parameter \'x_0\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--y', default=str(40**10), required=False,
                        help='parameter \'x_1\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.x, args.y, args.output_file


def bbsg(n, x, y, seed=random.randint(1, 1e10)):

    def next_usable_prime(x):
        p = sympy.nextprime(x)
        while p % 4 != 3:
            p = sympy.nextprime(p)
        return p

    random_numbers = []
    p = next_usable_prime(x)
    q = next_usable_prime(y)
    M = p * q
    for i in range(n):
        x = seed
        bit_output = ""
        for _ in range(n):
            x = x*x % M
            b = x % 2  # ostatni bit (reszty z dzielenia przez M w zapisie bin)
            bit_output += str(b)
    return bit_output


n, x, y, output_file = ParseArguments()

n = int(n)
x = int(x)
y = int(y)
M, numbers = 2, bbsg(n, x, y)

if output_file == "":
    print("Wygenerowane bity: \n", numbers)
else:
    data = {'n': n,
            'Modulus': M,
            'numbers': numbers}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)


print(numbers)
