from passwordvault import PasswordVault

print("Enter salt:")
salt = input()

v = PasswordVault()
v.initEncryption(salt)
v.startDisplay()
