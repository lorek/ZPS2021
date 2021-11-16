import argparse
import pickle


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="1000", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--x_0', default="1000", required=False,
                        help='parameter \'x_0\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--x_1', default="1430", required=False,
                        help='parameter \'x_1\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--M', default="1002", required=False,
                        help='Modulus \'M\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.x_0, args.x_1, args.M, args.output_file


def fibo_random_gen(n, x_0=1000, x_1=1430, M=1002):
    random_numbers = [0] * n
    for i in range(n):
        x_0, x_1 = x_1, (x_0 + x_1) % M
        random_numbers[i] = x_1
    return random_numbers


n, x_0, x_1, M, output_file = ParseArguments()

n = int(n)
x_0 = int(x_0)
x_1 = int(x_1)
M = int(M)

numbers = fibo_random_gen(n, x_0, x_1, M)

if output_file == "":
    print("Wygenerowane liczby: \n", numbers)
else:
    data = {'n': n,
            'Modulus': M,
            'numbers': numbers}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)

print(numbers)
