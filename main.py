from passwordvault import PasswordVault
import sys

salt = sys.argv[1]
v = PasswordVault()
v.initEncryption(salt)
v.startDisplay()
