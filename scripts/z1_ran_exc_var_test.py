import numpy as np
from scipy import special
import argparse
import pickle
import pandas as pd
import os
import platform


# Sample usage:

# python  z1_ran_exc_var_test.py --input-file generated_numbers.pkl
# python  z1_ran_exc_var_test.py --input-file test.pkl --output-file ran_exc_var_p-values.pkl

# jesli output_file jest pusty, to p-wartosci zostana wyswietlone, w przeciwnym przypadku zapisane do pliku


def ParseArguments():
    parser = argparse.ArgumentParser(description="Project")
    parser.add_argument('--input-file', default="generated_numbers.pkl", required=False, help='input file (default: %(default)s)')
    parser.add_argument('--input-dir', default="", required=False, help='input directory (default: %(default)s)')
    parser.add_argument('--output-file', default="ran_exc_var_p_values.csv", required=False, help='output file (default: %(default)s)')
    args = parser.parse_args()

    return args.input_file, args.input_dir, args.output_file


input_file, input_dir, output_file = ParseArguments()


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


#tworzenie dataframe dla p wartosci
df = {'p-9': [], 'p-8': [],'p-7': [], 'p-6': [], 'p-5': [], 'p-4': [], 'p-3': [], 'p-2': [], 'p-1': [], 'p+1': [], 'p+2': [], 'p+3': [], 'p+4': [], 'p+5': [], 'p+6': [], 'p+7': [],'p+8': [], 'p+9': []}
p_values_df = pd.DataFrame(data=df)

#wyznaczanie p-wartosci

#gdy z pliku
if(input_dir == ""):
    numbers_info = pd.read_pickle(input_file)
    M = numbers_info["Modulus"]
    numbers = numbers_info['numbers']

    nr_digits = int(np.log2(M))

    p_values = ran_exc_var(numbers, nr_digits)
    p_values_df.loc[len(p_values_df)] = p_values

#gdy z folderu
else:
    files = os.listdir(input_dir)

    if (input_dir != ""):
        if (platform.system() == "Windows"):
            input_dir += "\\"
        else:
            input_dir += "/"

    for file in files:
        numbers_info = pd.read_pickle(input_dir+file)
        M = numbers_info["Modulus"]
        numbers = numbers_info['numbers']
        nr_digits = int(np.log2(M))

        p_values = ran_exc_var(numbers, nr_digits)
        p_values_df.loc[len(p_values_df)] = p_values


#zapiswanie do pliku lub wyswietlanie
if output_file == "":
    print("Otrzymane p-wartosci: \n")
    print(p_values_df)
else:
    p_values_df.to_csv(output_file, index=False)
    print("P-wartosci zapisano w: ", output_file)