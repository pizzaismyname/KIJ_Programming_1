from BitVector import *
import binascii, numpy as np
import random, struct, copy

class AES():
    rounds = 10 # 128 bit keys -> 10 rounds

    def __init__(self, key, plaintext):
        self.round_const = BitVector(intVal=0x01, size=8)
        self.modulus = BitVector(bitstring='100011011')
        self.Sbox = gen_Sbox(self.modulus)

        round_key_count = (self.rounds + 1) * 4
        key_words = gen_key(key, self.modulus, self.round_const, self.Sbox, round_key_count)

        round_keys = [None for i in range(self.rounds+1)]

        for i in range(self.rounds+1):
            round_keys[i] = key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3]
            round_keys[i] = round_keys[i].get_bitvector_in_hex()

        for round_key in round_keys:
            print(round_key)
        self.round_keys = round_keys

    def encrypt(self, plaintext=""):
        if len(plaintext)//8 != 16:
            raise ValueError('block size not correct')

def gen_Sbox(modulus):
    sbox = list()
    c = BitVector(bitstring='01100011')
    
    for i in range(256):
        if i == 0:
            b_prime = BitVector(intVal = 0, size = 8)
        else:
            b_prime = BitVector(intVal=i, size=8).gf_MI(modulus, 8)
        b1, b2, b3, b4 = [b_prime.deep_copy() for _ in range(4)]
        b_prime ^= (b1 >> 4) ^ (b2 >> 5) ^ (b3 >> 6) ^ (b4 >> 7) ^ c
        sbox.append(int(b_prime))
    return sbox

def gen_Gfunc(keyword, rconst, Sbox, modulus):
    tmp = keyword.deep_copy()
    # keyword * 2^8
    tmp << 8
    word = BitVector(size=0)
    for i in range(4):
        word += BitVector(intVal = Sbox[tmp[i*8:i*8+8].intValue()], size = 8)
    #     print(word)
    # print("LEN\n")
    # print(len(word[:9]), len(rconst))
    word[:9] ^= rconst
    rconst = rconst.gf_multiply_modular(BitVector(intVal = 0x02), modulus, 8)
    return word, rconst

# Key Expansion
def gen_key(key, round_const, modulus, sbox, round_key_count):
    key_words = [None for _ in range(round_key_count)]
    rconst = round_const.deep_copy()
    # First 4 bits key insert to key word
    for i in range(4):
        key_words[i] = key[i*32:i*32+32]
    for i in range(4, 44):
        tmp = key_words[i-1]
        if i%4 == 0:
            # print("Keywords {}\n".format(key_words[i-1]))
            word, round_const = gen_Gfunc(tmp, rconst, sbox, modulus)
            key_words[i] = key_words[i-4] ^ word
        else:
            key_words[i] = key_words[i-4] ^ tmp

    return key_words

def main():
    key_input = input('Input the key: ')
    plaintext = input('Input plaintext: ')

    # Remove space trailing from key
    key_input = key_input.strip()

    len_key = len(key_input)

    # Insert 0 if keysize not 128 bits
    if len_key < 128//8:
        key_input += '0'*(128//8-len_key)
    else: # if more than 128 bits, trim the key
        key_input = key_input[:128//8]

    # Convert to hexadecimal
    int_key = int.from_bytes(key_input.encode(), 'big')
    print("Key in hexadecimal : {}\n".format(hex(int_key)))
    # key_bits = bin(hex_key)
    key_bits = BitVector(textstring=key_input)

    aes = AES(key_bits, plaintext)




main()