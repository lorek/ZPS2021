from math import ceil, floor, log2

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
    
if __name__ == '__main__':
    print("Good bits ---------------------")
    bits1 = '0101111101000101'
    ints1 = bits_to_ints(bits1, 8)
    bits2 = ints_to_bits(ints1,2)
    print(bits1, ints1, bits1 == bits2)
    bits1 == bits2
    # print("\nBad bits --------------------")
    # bad_bits = '01011111010001011'
    # ints2 = bits_to_ints(bad_bits, 1)
    ints2 = bits_to_ints(bits1, 30)
    print(ints2)