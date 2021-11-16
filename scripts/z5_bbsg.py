# https://asecuritysite.com/encryption/blum

import sympy
import random


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / gcd(a, b)


def gcd(a, b):
    """Compute the greatest common divisor of a and b"""
    while b > 0:
        a, b = b, a % b
    return a


def next_usable_prime(x):
    p = sympy.nextprime(x)
    while (p % 4 != 3):
        p = sympy.nextprime(p)
    return p


def bbsg(x, y, m, seed=random.randint(1, 1e10)):
    p = next_usable_prime(x)
    q = next_usable_prime(y)
    M = p*q

    x = seed

    bit_output = ""
    for _ in range(m):
        x = x*x % M
        b = x % 2
        bit_output += str(b)
    return bit_output


if __name__ == '__main__':
    x = 3*10**10
    y = 4*10**10

    print(bbsg(x, y, 100))
