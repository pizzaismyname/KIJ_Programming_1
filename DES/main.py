import encrypt as enc
import initial as init


key = input("Enter your key: ")
plainText = input("Enter your plain text: ")
if init.key_check(key) == True:
    
    if len(plainText) % 8 != 0:
        plainText += " "
    cipherText = enc.encrypt(key, plainText)
    print(cipherText)
