from cryptography.fernet import Fernet
import os


"""
 Creating Encription key and store It
"""


def create_key():
    key = Fernet.generate_key()
    PATH = 'key.key'
    if not os.path.isfile(PATH) and not os.access(PATH, os.R_OK):
        file = open('key.key', 'wb')
        file.write(key)
        file.close()


"""
 Getting the encryption key in the file
"""


def get_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


# """
#  Encrypting Text
# """
#
#
# def encrypt_text(text):
#
#     encoded_text = text.encode()
#     f = Fernet(get_key())
#     encrypted_text = f.encrypt(encoded_text)
#     return encrypted_text
# #
# """
# Decrypting text
# """
#
#
# def decrypt_text(encrypted_text):
#
#     try:
#         f = Fernet(get_key())
#
#         decrypted_text = f.decrypt(encrypted_text)
#         return decrypted_text
#     except Exception as e:
#         print(str(e))


