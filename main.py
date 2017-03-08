#!/usr/bin/env python3
import os
import secrets

class Trivium:
    def __init__(self, pt="", ct="", key="", keystream="", IV=""):
        self.pt = pt
        self.ct = ct
        self.keystream = keystream
        self.key = key
        self.IV = IV

    def encrypt(self):
        A = [0 for x in range(93)]
        B = [0 for x in range(84)]
        C = [0 for x in range(111)]

        if len(self.IV) != 80 or len([x for x in self.IV if x in "10"]) != len(self.IV):
            raise IVErrorException("An 80-bit IV is required, represented as a binary string, i.e '010101...'."\
                                   "A IV can be generated if the argument 'gen_IV=1' is passed to encrypt method.")
        if len(self.key) != 80 or len([x for x in self.key if x in "10"]) != len(self.key):
            raise Exception("Key error.")

        #load IV into registers
        for i in range(80): A[i] = self.IV[i]
        for i in range(80): B[i] = self.key[i]
        for i in range(108, 111): C[i] = "1"

        #warm-up phase, cipher ran 1152 times to ensure keystream is a product of both the IV and key
        for i in range(1152):
            #A - Input

            #B - Input

            #C - input


    def decrypt(self):
        pass

    def gen_key_stream(self, size):
        pass

class IVErrorException(Exception):
    pass

if __name__ == '__main__':
    pt = "Hello World!"
    IV = "11101011110000100000110001011001111011110010100001110100000011001100010111000000"
    key = "10101000000001011000110101101101110011000000100001101010110101101111001100101001"
    t = Trivium(pt=pt, key=key, IV=IV)
    ct = t.encrypt()
    print(ct)
