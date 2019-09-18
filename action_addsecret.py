from passwordvault import PasswordVault
import sys
import os

if len(sys.argv) == 4:
    key = sys.argv[1]
    secret = sys.argv[2]
    salt = sys.argv[3]
    try:
        vault = PasswordVault()
        vault.initEncryption(salt)
        vault.addSecret(key, secret)
        print("added")
    except:
        print("failed")
else:
    print("failed")