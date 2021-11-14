from math import ceil, floor, log2
import numpy as np

def is_power_of_two(n: int) -> bool:
    """Check if number is power of 2"""
    return (ceil(log2(n)) == floor(log2(n)))

def bits_to_ints(bits: str, n: int) -> list:
    """Convert string representing bits into array of n integers."""
    k = len(bits)/n # how many bits for each number?
    if not is_power_of_two(k):
        raise ValueError(f"Number of bits divided by n (now {k}) must be power of 2.")
    else:
        k = int(k)
        return [int(bits[i:i+k],2) for i in range(0, len(bits)-k+1, k)]

def ints_to_bits(ints: list, k: int) -> str:
    """Convert array of ints into string of bits (k bits for each number)"""
    bits = ''
    for x in ints:
        bits += format(x, "b").zfill(k)
    return bits


def ints_to_floats(ints: np.ndarray, k: int, a:float = 0, b:float = 1) -> np.ndarray:
    """Convert array of integers from {0, ... k} to floats in range [a,b]"""
    floats = []
    for i,x in enumerate(ints):
        if x > k: 
            raise ValueError(f"{x} (on position {i}) is not a number from 0, ... {k}")
        u_0_1 = x/k 
        floats.append(u_0_1 * (b-a) + a)  
    return np.asarray(floats)

    
if __name__ == '__main__':
    ints = np.array([1, 3, 9, 0, 6, 8, 8, 9])
    print(f"ints_to_floats: {ints_to_floats(ints, 10, 0.5, 0.8)}")
    # print("Good bits ---------------------")
    # bits1 = '0101111101000101'
    # ints1 = bits_to_ints(bits1, 8)
    # bits2 = ints_to_bits(ints1,2)
    # print(bits1, ints1, bits1 == bits2)
    # bits1 == bits2
    
    # print("\nBad bits --------------------")
    # bad_bits = '01011111010001011'
    # ints2 = bits_to_ints(bad_bits, 1)
    # ints2 = bits_to_ints(bits1, 30)
    # print(ints2)