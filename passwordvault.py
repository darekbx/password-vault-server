# Requirements
# python3 -m pip install cryptography
# python3 -m pip install psutil

from encryption import Encryption
from storage import Storage
from mainmenu import MainMenu

class PasswordVault:

    storage_file = "/home/pi/password-vault-server/vault.json"

    storage = None
    encryption = None
    main_menu = None

    def __init__(self):
        self.storage = Storage(self.storage_file)
    
    def startDisplay(self):
        self.main_menu = MainMenu()
        self.main_menu.init()
        self.main_menu.secretsCallback = self.listSecrets
        self.main_menu.secretCallback = self.retrieveSecret
        self.main_menu.display()

    def initEncryption(self, salt):
        self.encryption = Encryption(salt)

    def addSecret(self, key, secret):
        encoded_secret = self.encryption.encode(secret)
        secrets = self.storage.read()
        secrets[key] = encoded_secret
        self.storage.save(secrets)
    
    def listSecrets(self):
        secrets = self.storage.read()
        return list(secrets.keys())

    def retrieveSecret(self, key):
        secrets = self.storage.read()
        hashed_secret = secrets[key]
        decoded_secret = self.encryption.decode(hashed_secret)
        return decoded_secret
