# coding:utf-8
import hashlib


class PasswordContext(object):
    def __init__(self, password_prefix):
        self.password_prefix = password_prefix

    def verify_password(self, secret, hashed):
        secret_hashed = self.encrypt(secret)
        if secret_hashed == hashed:
            return True
        else:
            return False


    def encrypt(self, secret):
        hashed = hashlib.sha1(
            self.password_prefix + hashlib.sha1(self.password_prefix + secret).hexdigest()
        ).hexdigest();
        return hashed;



