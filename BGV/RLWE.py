import numpy as np
import random
import math
import sys

def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True
        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)

    return prime_list

def encode(plaintext):
    bin_arr = bytearray(plaintext, 'utf-8')
    res = []
    bin_str=''
    for bit in bin_arr:
        binary_rep = format(bit,'08b')
        #print(binary_rep)
        res.append(binary_rep)
    bin_str = bin_str.join(res)
    length = len(bin_str)

    return bin_str, length

