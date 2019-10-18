import encrypt as enc
import decrypt as dec
import initial as init


key = input("Enter your key (only 8 chars will be used): ")
plainText = input("Enter your plain text (only 8 chars will be used): ")
key = init.key_check(key)
# if init.key_check(key) == True:
if len(plainText) < 8:
    plainText += '0'*(56//8-len(plainText)+1)
elif len(plainText) > 8:
    plainText = plainText[:8]

cipherText = enc.encrypt(key, plainText)
print("Cipher text yang dihasilkan> %r" %cipherText)
hasilDec = dec.decrypt(key, cipherText)
print("Hasil dekripsi menghasilkan> ", hasilDec)
