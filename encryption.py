from cryptography.fernet import Fernet
import base64
import debug

class Encryption:

    _saltPrefixFile = "/home/pi/password-vault-server/salt_prefix" if not debug.isDebug() else "salt_prefix"
    _encoding = "utf-8"
    _saltEncoding = "ascii"
    _saltPrefix = None

    _salt = None
    
    def __init__(self, salt):
        """
        Parameters
        ----------
        salt : str
            The four character salt
        """
        with open(self._saltPrefixFile, "r") as handle:
            self._saltPrefix = handle.readline().rstrip()
        self._salt = salt

    def validate(self, hash):
        try:
            self.decode(hash)
            return True
        except:
            return False

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
        salt = "{0}{1}".format(self._saltPrefix, self._salt).encode(self._saltEncoding)
        return base64.urlsafe_b64encode(salt)
