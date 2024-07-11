import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


def encrypt(key_path, msg_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    with open(msg_path, 'rb') as o_file:
        data = o_file.read()

    nonce = secrets.token_bytes(12)
    cipher_data = nonce + AESGCM(key).encrypt(nonce, data, b'')

    with open(msg_path, 'wb') as enc_file:
        enc_file.write(cipher_data)


def decrypt(key_path, msg_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()

    with open(msg_path, 'rb') as enc_file:
        encrypted = enc_file.read()

    data = AESGCM(key).decrypt(encrypted[:12], encrypted[12:], b'')

    with open(msg_path, 'wb') as dec_file:
        dec_file.write(data)


def generate_new_key(key_path):
    key = secrets.token_bytes(32)

    with open(key_path, 'wb') as key_file:
        key_file.write(key)


user_input = input('What would you like me to do? \nEnter "encrypt" or "decrypt": \n').lower()

decrypted_folder = 'decrypted'
encrypted_folder = 'encrypted'

if user_input == 'encrypt':
    if os.listdir('decrypted'):
        for file in os.listdir('decrypted'):
            encrypt('key/cipher_key.txt', f'{decrypted_folder}/{file}')
            os.replace(f'{decrypted_folder}/{file}',
                       f'{encrypted_folder}/{file}')
        print('All files encrypted and moved to encrypted directory.')
    else:
        print('No files to encrypt.')

elif user_input == 'decrypt':
    if os.listdir('encrypted'):
        for file in os.listdir('encrypted'):
            decrypt('key/cipher_key.txt', f'{encrypted_folder}/{file}')
            os.replace(f'{encrypted_folder}/{file}',
                       f'{decrypted_folder}/{file}')
        print('All files decrypted and moved to decrypted directory.')
    else:
        print('No files to decrypt.')

else:
    print('You need to enter "encrypt" or "decrypt".')
