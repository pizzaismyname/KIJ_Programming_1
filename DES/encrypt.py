import itertools as it
from initial import *

def encrypt(key, text):
    print("Generate key....")
    keyBit = list()
    result = list()
    for char in key:
        binVal = binValue(char, 8)
        keyBit.extend([int(i) for i in list(binVal)])
    keyBit = [keyBit[i-1] for i in permutChoice1]
    leftKey, rightKey = [keyBit[i:i+28] for i in range(0, len(keyBit), 28)]
    for i in range(16):
        leftKey, rightKey = leftKey[shiftMat[i]:] + leftKey[:shiftMat[i]], rightKey[shiftMat[i]:] + rightKey[:shiftMat[i]]
        tmp = leftKey + rightKey
        keyBit.append([tmp[i-1] for i in permutChoice2])

    print("Jalankan setiap ronde....")
    textBlock = [text[i:i+8] for i in range(0, len(text), 8)]
    for block in textBlock:
        blockBit = list()
        for char in block:
            binVal = binValue(char, 8)
            blockBit.extend([int(i) for i in list(binVal)])
            
        blockBit = [blockBit[i-1] for i in initPermut]
        left, right = [blockBit[i:i+32] for i in range(0, len(blockBit), 32)]
        tmp = None
        for i in range(16):
            rightExpand = [right[i-1] for i in expand]
            tmp = [i^j for i,j in zip(it.repeat(keyBit[i], len(rightExpand)), rightExpand)]
        tmp = substitute(tmp)
        tmp = [tmp[i-1] for i in permut]
        tmp = [i^j for i,j in zip(it.repeat(left[i], len(tmp)), tmp)]
        left = right
        right = tmp
    result += [(right+left)[i-1] for i in finalPermut]
    
    hasil = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in  [result[i:i+8] for i in range(0, len(result), 8)]]])
    
    print("Selesai!")
    return hasil
            
    
