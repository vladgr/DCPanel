import base64
from django.conf import settings
from django import forms
from Crypto.Cipher import AES


def encrypt(text):
    """text (string)"""
    aes = AES.new(settings.CRYPT_KEY, AES.MODE_CFB, settings.CRYPT_IV)
    return base64.b64encode(aes.encrypt(text.encode())).decode()


def decrypt(text):
    """Returns original string"""
    text = base64.b64decode(text.encode())
    aes = AES.new(settings.CRYPT_KEY, AES.MODE_CFB, settings.CRYPT_IV)
    return aes.decrypt(text).decode()


class TextareaXL(forms.Textarea):

    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault('attrs', {})
        attrs.setdefault('cols', 140)
        attrs.setdefault('rows', 30)
        super(TextareaXL, self).__init__(*args, **kwargs)
