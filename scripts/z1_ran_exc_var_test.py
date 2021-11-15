import numpy as np
from scipy import special
import argparse
import pickle
import pandas as pd


# Sample usage:

# python  z1_ran_exc_var_test.py --input-file generated_numbers.pkl
# python  z1_ran_exc_var_test.py --input-file test.pkl --output-file ran_exc_var_p-values.pkl

# jesli output_file jest pusty, to p-wartosci zostana wyswietlone, w przeciwnym przypadku zapisane do pliku


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False,
                        help='output file (default: %(default)s)')
    parser.add_argument('--output-file', default="ran_exc_var_p_values.pkl", required=False,
                        help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.output_file


input_file, output_file = ParseArguments()

numbers_info = pd.read_pickle(input_file)
M = numbers_info["Modulus"]
numbers = numbers_info['numbers']

nr_digits = int(np.log2(M))

#Implementacji random excursions variance test
def ran_exc_var(numbers, nr_digits):
    appearances = np.zeros(19) #do liczenia wystepowania wartosci od -9 do 9
    summed = 0
    for number in numbers:
        nr_binary_text = np.binary_repr(number)
        binary_text_len = len(nr_binary_text)
        fill_array = np.zeros(nr_digits - binary_text_len) - 1 #korekta na brakujace zera (minus jedynki) na poczatku liczby
        nr_corrected = 2 * np.array(list(map(int, list(nr_binary_text)))) - 1
        nr_corrected = np.concatenate((fill_array, nr_corrected))
        for i in nr_corrected:
            summed += int(i)
            if(summed >= -9 and summed <= 9):
                appearances[summed + 9] += 1 #+9 pozwala przeliczac wartosci -9 do 9 na indeksy 0 do 18
    if(summed != 0):
        appearances[9] += 1     #zwieksz ilosc cykli o jeden jezeli na koncu nie ma zera
    values = np.absolute(np.arange(-9, 10))
    values[9] = 1 #wartosc dla zera jest nieistotna dla testu, a pozostawienie jej skutkuje bledem w nastepnej lini (ujemna liczba pod pierwiastkiem)
    vec_for_erfc = (np.absolute(appearances - appearances[9]))/(np.sqrt(2 * appearances[9] * (4 * values - 2))) #wektor wartosci podstawianych do erfc
    p_values = special.erfc(vec_for_erfc) #wyznaczamy wektor 18 p-wartosci za pomoca funkcji erfc
    p_values_list = list(p_values)
    del p_values_list[9] #usuwamy p wartosc dla zera, poniewaz jest zbedna w tym tescie
    return p_values_list


p_values = ran_exc_var(numbers, nr_digits)

if output_file == "":
    print("Otrzymane p-wartosci: \n", p_values)
else:

    data = {'Test':  "Random Excursions variance test",
            'p-values': p_values}

    data_outfile = open(output_file, 'wb+')
    pickle.dump(data, data_outfile)
    print("P-wartosci zapisano w: ", output_file)
