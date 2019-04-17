#python imports
import base64
from hashlib import sha256

#django imports
from django.conf import settings

#local imports

#inter app imports

#third party imports
from Crypto.Cipher import AES

class EpayLaterEncryptDecryptUtil(object):
    
    def __init__(self, key, iv):
        self.bs = 16
        self.key = key
        self.iv = iv
    
    def checksum(self, raw):
        return sha256(raw).hexdigest().upper()
    
    def encrypt(self, raw):
        raw = self._pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))
        
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return self._unpad(cipher.decrypt(enc)).decode('utf-8')
    
    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) %self.bs).encode('utf-8')
    
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]