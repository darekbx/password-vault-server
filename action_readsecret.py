from passwordvault import PasswordVault
import sys
import os

if len(sys.argv) == 3:
    key = sys.argv[1]
    salt = sys.argv[2]
    try:
        vault = PasswordVault()
        vault.initEncryption(salt)
        secret = vault.retrieveSecret(key)
        print(secret)
    except:
        print("failed")
else:
    print("failed")