#!/usr/bin/env python3
import os
import secrets
import base64

#NOTE: Unsure whether secure or not, so assume it's not and use for demo purposes only
class Trivium:
    def __init__(self, pt="", ct="", key="", keystream="", IV=""):
        self.pt = pt
        self.ct = ct
        self.keystream = keystream
        self.key = key
        self.IV = IV

    def encrypt(self):
        self.load_regs()

        pt_bin = ""
        for i in self.pt:
            b = bin(ord(i))[2:]
            pt_bin += ("0" * (7 - len(b))) + b
        pt_bin = [int(x) for x in pt_bin]

        key_stream = [self.cycle() for x in range(len(pt_bin))]
        ct = "".join([str((key_stream[x] + pt_bin[x]) % 2) for x in range(len(pt_bin))])
        ct = "".join([chr(int(ct[x:x + 7], 2)) for x in range(0, len(ct), 7)])
        return str(base64.b64encode(bytes(ct, "utf-8")))[2:-1]

    def decrypt(self):
        self.load_regs()

        d = base64.b64decode(self.ct).decode("utf-8")
        ct = ""
        for i in d:
            b = bin(ord(i))[2:]
            ct += ("0" * (7 - len(b))) + b
        ct = [int(x) for x in ct]

        key_stream = [self.cycle() for x in range(len(ct))]
        pt = "".join([str((key_stream[x] + ct[x]) % 2) for x in range(len(ct))])
        pt = "".join([chr(int(pt[x:x + 7], 2)) for x in range(0, len(pt), 7)])
        return pt

    def load_regs(self):
        self.A = [0 for x in range(93)]
        self.B = [0 for x in range(84)]
        self.C = [0 for x in range(111)]

        #load IV into registers
        for i in range(80): self.A[i] = int(self.IV[i])
        for i in range(80): self.B[i] = int(self.key[i])
        for i in range(108, 111): self.C[i] = 1

        #warm-up phase, cipher ran 1152 times to ensure keystream is a product of both the IV and key
        for i in range(1152): self.cycle()

    def cycle(self):
        a_out = (self.A[92] + self.A[65] + (self.A[90] & self.A[91])) % 2
        b_out = (self.B[83] + self.B[68] + (self.B[81] & self.B[82])) % 2
        c_out = (self.C[110] + self.C[65] + (self.C[108] & self.C[109])) % 2
        out = (a_out + b_out + c_out) % 2

        a_in = (c_out + self.A[68]) % 2
        b_in = (a_out + self.B[77]) % 2
        c_in = (b_out + self.C[86]) % 2

        del self.A[-1]
        del self.B[-1]
        del self.C[-1]

        self.A = [a_in] + self.A
        self.B = [b_in] + self.B
        self.C = [c_in] + self.C

        return out

    def gen_key_stream(self, size):
        pass

class IVErrorException(Exception):
    pass

if __name__ == '__main__':
    pt = "Hello World!, how are you?"
    ct = "cQ5ZXyUtJUlGXDhhFBkcS3hmTg9lf35dTWw="
    IV = "11101011110000100000110001011001111011110010100001110100000011001100010111000000"
    key = "10101000000001011000110101101101110011000000100001101010110101101111001100101001"
    t = Trivium(ct=ct, key=key, IV=IV)
    print(t.decrypt())
