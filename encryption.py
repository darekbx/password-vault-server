from cryptography.fernet import Fernet
import base64

class Encryption:

    _encoding = "utf-8"
    _saltEncoding = "ascii"
    _saltSufix = "hXjJGMdKegjLIYmQrnEMIpDrjpR_"

    _salt = None
    
    def __init__(self, salt):
        """
        Parameters
        ----------
        salt : str
            The four character salt
        """
        self._salt = salt

    def encode(self, secret):
        salt = self._createSalt()
        fernet = Fernet(salt)
        hashedSecret = fernet.encrypt(secret.encode(self._encoding))
        return hashedSecret.decode(self._encoding)

    def decode(self, hashed_secret):
        salt = self._createSalt()
        fernet = Fernet(salt)
        decodedSecret = fernet.decrypt(hashed_secret.encode(self._encoding))
        return decodedSecret.decode(self._encoding)

    def _createSalt(self):
        salt = "{0}{1}".format(self._saltSufix, self._salt).encode(self._saltEncoding)
        return base64.urlsafe_b64encode(salt)