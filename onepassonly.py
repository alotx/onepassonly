import hashlib
from base64 import b64encode


class OnePassOnly:

    def __init__(self):
        self._hash_algo = 'sha256'
        self._encoding = 'latin-1'

    def setup(self, **kwargs):
        for key in kwargs.keys():
            if key == 'hash_algo':
                self._hash_algo = kwargs[key]
            elif key == 'encoding':
                self._encoding = kwargs[key]
            else:
                raise ValueError

    def genpass(self, login, secret, length=16):
        """
         Generates a password based on the account and a common secret
         :param login: The site's account name (e.g. johndoe@none.org)
         :param secret: Unique password to use
         :param length: The length of the resulting password 
         :return: The password to be used.
         """
        text = login + secret
        m = hashlib.new(self._hash_algo)
        m.update(text.encode(self._encoding))
        return b64encode(m.digest())[:length].decode()