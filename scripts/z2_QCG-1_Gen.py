import argparse
import pickle


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--n', default="1000", required=False, help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--x_0', default="984", required=False,
                        help='parameter \'x_0\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--p', default="709", required=False,
                        help='Modulus \'p\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.x_0, args.p, args.output_file


def QCG_I(n, x_0=984, p=709):
    qcg_numbers = [0] * n
    for i in range(n):
        x_0 = (x_0 ** 2) % p
        qcg_numbers[i] = x_0
    return qcg_numbers


n, x_0, p, output_file = ParseArguments()

n = int(n)
x_0 = int(x_0)
p = int(p)

numbers = QCG_I(n, x_0, p)

if output_file == "":
    print("Wygenerowane liczby: \n", numbers)
else:
    data = {'n': n,
            'Modulus': p,
            'numbers': numbers}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("Wygenerowane liczby zapisano w: ", output_file)

print(numbers)
