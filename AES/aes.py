from BitVector import *
import binascii, numpy as np
import random, struct, copy
from collections import deque

class AES():
    rounds = 10 # 128 bit keys -> 10 rounds

    def __init__(self, key, plaintext):
        self.__plaintext = plaintext
        self.__key = key
        self.round_const = BitVector(intVal=0x01, size=8)
        self.modulus = BitVector(bitstring='100011011')
        self.Sbox = gen_Sbox(self.modulus)
        # print(self.Sbox)

        round_key_count = (self.rounds + 1) * 4
        key_words = gen_key(key, self.modulus, self.round_const, self.Sbox, round_key_count)

        round_keys = [0 for i in range(self.rounds+1)]
        key_schedule = list()

        for i in range(self.rounds+1):
            round_keys[i] = key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3]
            round_keys[i] = round_keys[i].get_bitvector_in_hex()
        
        for _, k in enumerate(key_words):
            int_keys = list()
            for i in range(4):
                int_keys.append(k[i*8:i*8+8].intValue())
            key_schedule.append(int_keys)
        
        self.key_schedule = key_schedule
        # for round_key in round_keys:
        #     print(round_key)
        # print(round_keys[0])
        for i in range(len(round_keys)):
            round_keys[i] = text2matrix(int(round_keys[i], 16))
        self.round_keys = round_keys[0]
        # print(round_keys[0])
        # for i in range(1, 10):
        #     print(self.round_keys[i*4:(i+1)*4])
        # for i in range(4):
        #     for j in range(4):
        #         print(self.__plaintext[i][j] ^ self.round_keys[i][j])

    def encrypt(self):
        # print(len(self.__plaintext))
        # if len(self.__plaintext)//8 != 16:
        #     raise ValueError('block size not correct')
        statearray = self.round_key(self.__plaintext, self.key_schedule[:4])
        
        for i in range(1, self.rounds):
            self.subBytes(statearray)
            self.shiftRow(statearray)
            mixed = self.mixColumn(statearray)
            statearray = self.round_key(mixed, self.key_schedule[i*4:(i+1)*4])

        # final round
        self.subBytes(statearray)
        self.shiftRow(statearray)
        self.round_key(statearray, self.key_schedule[40:])

        return statearray

    def decrypt(self):
        pass

    def round_key(self, text, keys):
        # print(type(keys[0][0]), type(text[0][0]))
        statearray = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                # pass
                statearray[i][j] = text[i][j] ^ keys[i][j]
                # print(self.__plaintext[i][j] ^ self.round_keys[i][j])
        return statearray

    def subBytes(self, text):
        # tmp = text.copy()
        # tmp << 8
        # tmp2 = BitVector(size=0)
        for i in range(4):
            for j in range(4):
                text[i][j] = self.Sbox[text[i][j]]
        #     tmp2 += BitVector(intValue=self.Sbox[tmp[i*8:i*8+8]], size=8)
        # print(tmp2)

    def shiftRow(self, statearray):
        statearray[0][1], statearray[1][1], statearray[2][1], statearray[3][1] = statearray[1][1], statearray[2][1], statearray[3][1], statearray[0][1]

        statearray[0][2], statearray[1][2], statearray[2][2], statearray[3][2] = statearray[2][2], statearray[3][2], statearray[0][2], statearray[1][2]

        statearray[0][3], statearray[1][3], statearray[2][3], statearray[3][3] = statearray[3][3], statearray[0][3], statearray[1][3], statearray[2][3]

    def mixColumn(self, statearray):
        tmp = [[0 for _ in range(4)] for _ in range(4)]
        op = [
            [0x02, 0x03, 0x01, 0x01],
            [0x01, 0x02, 0x03, 0x01],
            [0x01, 0x01, 0x02, 0x03], 
            [0x03, 0x01, 0x01, 0x02]
        ]

        for i in range(4):
            for j in range(4):
                tmp[i][j] = op[i][j] ^ statearray[i][j]

        return tmp

    def invMixColumn(self, statearray):
        tmp = list()
        op = [
            [0x0E, 0x0B, 0x0D, 0x09],
            [0x09, 0x0E, 0x0B, 0x0D],
            [0x0D, 0x09, 0x0E, 0x0B],
            [0x0B, 0x0D, 0x09, 0x0E]
        ]

        for i in range(4):
            for j in range(4):
                tmp[i][j] = op[i][j] ^ statearray[i][j]

        return tmp

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

def text2matrix(text):
    matrix = []
    for i in range(16):
        byte = (text >> (8 * (15 - i))) & 0xFF
        if i % 4 == 0:
            matrix.append([byte])
        else:
            matrix[i // 4].append(byte)
    return matrix

def matrix2text(matrix):
    text = 0
    for i in range(4):
        for j in range(4):
            text |= (matrix[i][j] << (120 - 8 * (4 * i + j)))
    return text

def main():
    key_input = input('Input the key: ')
    plaintext = input('Input plaintext: ')

    # Remove space trailing from key
    key_input = key_input.strip()

    len_key = len(key_input)
    len_plaintext = len(plaintext)

    # Insert 0 if keysize not 128 bits
    if len_key < 128//8:
        key_input += '0'*(128//8-len_key)
    else: # if more than 128 bits, trim the key
        key_input = key_input[:128//8]

    if len_plaintext >= 128//8:
        plaintext = plaintext[:128//8]
    else:
        plaintext += '0'*(128//8-len_plaintext)

    # Convert to hexadecimal
    int_key = int.from_bytes(key_input.encode(), 'big')
    print("Key in hexadecimal : {}\n".format(hex(int_key)))
    # key_bits = bin(hex_key)
    key_bits = BitVector(textstring=key_input)
    # plaintext_bits = BitVector(textstring=plaintext)
    # print(hex(plaintext_bits.intValue()))
    hex_plaintext = hex(int.from_bytes(plaintext.encode(), 'big'))
    print("Plaintext in hexadecimal : {}\n".format(hex_plaintext))
    plaintext = text2matrix(int(hex_plaintext, 16))
    # print(plaintext)

    aes = AES(key_bits, plaintext)
    # test = matrix2text(aes.encrypt())
    test = aes.encrypt()
    tmp = []
    for i in range(len(test)):
        print(test[i])



main()
