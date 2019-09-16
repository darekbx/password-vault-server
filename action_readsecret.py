from passwordvault import PasswordVault
import sys
import os

if len(sys.argv) == 2:
    key = sys.argv[1]
    salt = os.environ[PasswordVault.salt_env_variable]
    try:
        vault = PasswordVault()
        vault.initEncryption(salt)
        secret = vault.retrieveSecret(key)
        print(secret)
    except:
        print("failed")
else:
    print("failed")