from passwordvault import PasswordVault
import sys
import os

if len(sys.argv) == 3:
    key = sys.argv[1]
    secret = sys.argv[2]
    salt = os.environ[PasswordVault.salt_env_variable]
    try:
        vault = PasswordVault()
        vault.initEncryption(salt)
        vault.addSecret(key, secret)
        print("added")
    except:
        print("failed")
else:
    print("failed")