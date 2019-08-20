# Requirements
# python3 -m pip install cryptography

from encryption import Encryption

class PasswordVault:

    storage_file = "vault.json"

    encrypted_storage = None

    def start(self, salt):
        self.encrypted_storage = Encryption(salt)
            
