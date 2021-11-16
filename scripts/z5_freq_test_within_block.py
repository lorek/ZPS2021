import math
import scipy.special as spc


def block_frequency(bin_data: str, block_size):
    M = len(bin_data)
    num_blocks = math.floor(M/block_size)  #ilość bloków
    block_start, block_end = 0, block_size
    proportion_sum = 0.0
    for i in range(num_blocks):
        block_data = bin_data[block_start:block_end]
        print(block_data)
        ones_count = 0
        for char in block_data:
            if char == '1':
                ones_count += 1
        pi = ones_count / block_size  # pi - proporcja jedynek w jednym bloku
        proportion_sum += pow(pi - 0.5, 2.0)  #suma( (pi-0.5)**2 )
        block_start += block_size
        block_end += block_size
    chi_squared = 4.0 * block_size * proportion_sum
    p_val = spc.gammaincc(num_blocks / 2, chi_squared / 2)
    return p_val


print(block_frequency('1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000',10))