import scipy.special as spc
import argparse
import pandas as pd
from scipy.stats import chisquare


def ParseArguments():
    parser = argparse.ArgumentParser(description="Second-level testing")
    parser.add_argument(
        "--input-file",
        default="p-values.csv",
        required=False,
        help="input file (default: %(default)s)",
    )
    parser.add_argument(
        "--output-file",
        default="p-values-final.csv",
        required=False,
        help="output file with final p-values (default: %(default)s)",
    )

    args = parser.parse_args()

    return args.input_file, args.output_file


def segegate_p_val(numbers):
    p1, p2, p3, p4, p5, p6, p7, p8, p9, p10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for p in numbers:
        if p >= 0.9:
            p10 += 1
        elif p >= 0.8:
            p9 += 1
        elif p >= 0.7:
            p8 += 1
        elif p >= 0.6:
            p7 += 1
        elif p >= 0.5:
            p6 += 1
        elif p >= 0.4:
            p5 += 1
        elif p >= 0.3:
            p4 += 1
        elif p >= 0.2:
            p3 += 1
        elif p >= 0.1:
            p2 += 1
        else:
            p1 += 1
    return [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]


if __name__ == "__main__":
    input_file, output_file = ParseArguments()
    pvalues = pd.read_csv(input_file)["p-value"].to_numpy()
    partitions = segegate_p_val(pvalues)

    # r = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    # chi_square = 0
    # for i in range(len(partitions)):
    #     chi_square += (partitions[i] + r[i] / 10) ** 2 / r[i]
    # p_val = spc.gammaincc(10 / 2, chi_square)

    e = round(
        len(pvalues) * 0.1,
    )
    chi_square, p_val = chisquare(partitions, [e for i in range(10)])
    print("p_value is: ", p_val)
    print("PRGN is not random :", p_val < 0.05)
    with open(output_file, "w") as f:
        f.write(str(p_val))
    print(f"p-value is saved in {output_file}.")
