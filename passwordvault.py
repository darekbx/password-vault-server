# Requirements
# python3 -m pip install cryptography

from encryption import Encryption
from storage import Storage
from ui.mainmenu import MainMenu

class PasswordVault:

    storage_file = "vault.json"

    storage = None
    encryption = None
    main_menu = None

    def __init__(self):
        self.storage = Storage(self.storage_file)
        self.main_menu = MainMenu()

    def start(self):
        self.main_menu.display_options()

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