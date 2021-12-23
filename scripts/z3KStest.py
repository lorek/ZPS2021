import scipy.stats as sts
import argparse
import pandas as pd
import glob

def ParseArguments():
    parser = argparse.ArgumentParser(description="Kolmogorov–Smirnov test")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='input file (default: %(default)s)')
    parser.add_argument('--input-dir', default="pickles_dir", required=False, help='input directory with .pkl files (default: %(default)s)')
    parser.add_argument('--pval-file', default="p-values.csv", required=False, help='output file with p-values (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.pval_file

input_file, input_dir, pval_file = ParseArguments()

if input_dir=="":
    numbers_info = pd.read_pickle(input_file)
    M = int(numbers_info['Modulus'])
    numbers = numbers_info['numbers'] #liczby (pseudolosowe)
    numbers = list(map(lambda x: x/M, numbers)) #zamiana na liczby z przedziału (0 , 1)
    test = sts.kstest(numbers, cdf = 'uniform')

    print("Kolmogorov–Smirnov test results:")
    print("p-value: "+str(test[1]))
    print("Statistic: "+str(test[0]))
    print("PARAMETERS:")
    print("M: "+str(numbers_info['Modulus']))
    print("n: "+str(numbers_info['n']))
    print("Numbers have beed generated with: "+str(numbers_info['PRNG']))
    pvals = []
    pvals.append(test[1])
    print("Saving p-value to ",pval_file)
    df=pd.DataFrame(pvals,columns=["p-value"])
    df.to_csv(pval_file, index = False)
else:
    print("input_dir = ", input_dir)
    pvals = []
    file_list = list((glob.glob(input_dir + "/**.pkl")))
    file_list.sort()
    for file_name in file_list:
        print("Processing file ", file_name, " ...")
        numbers_info = pd.read_pickle(file_name)
        M=numbers_info['Modulus']
        numbers = numbers_info['numbers']
        numbers = list(map(lambda x: x/M, numbers)) #zamiana na liczby z przedziału (0 , 1)
        test = sts.kstest(numbers, cdf = 'uniform')
        pvals.append(test[1])

    print("Saving p-values to ",pval_file)
    df=pd.DataFrame(pvals,columns=["p-value"])
    df.to_csv(pval_file, index = False)
