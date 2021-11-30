import random as r
import argparse
import pickle


def ParseArguments():
    parser = argparse.ArgumentParser(description="RC4 PRNG")
    parser.add_argument('--n', default='500', required=False,
                        help='nr of generated numbers (default: %(default)s)')
    parser.add_argument('--M', default=str(2**21), required=False,
                        help='Modulus \'M\' in PRNG recursion (default: %(default)s)')
    parser.add_argument('--K', default=r.sample(range(10000000), k=100), required=False,
                        help='seed (default: %(default)s)')
    parser.add_argument('--output-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.n, args.M, args.K, args.output_file


n, M, K, output_file = ParseArguments()

n = int(n)
M = int(M)


def RC4(n, M, K):

    def ksa(K):
        S = [i for i in range(M)]
        l = len(K)
        j = 0
        for i in range(M):
            j = (j + S[i] + K[i % l]) % M
            S[i], S[j] = S[j], S[i]
        return S

    def prga(n, M, S):
        x = []
        i, j = 0, 0
        for _ in range(n):
            i = (i + 1) % M
            j = (j + S[i]) % M
            S[i], S[j] = S[j], S[i]
            x.append(S[(S[i] + S[j]) % M])
        return x

    return prga(n, M, ksa(K))


numbers = RC4(n, M, K)

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
