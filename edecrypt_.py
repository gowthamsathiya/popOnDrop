"""
__author__ = Gowtham
__summary__ = Module to encrypt and decrypt the files. Used encryption type AES
__source__ = 'http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible'
__copyright__ = GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""

#import python modules
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import os

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]

def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = (bs - len(chunk) % bs) or bs
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))

def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)

password = 'hi'

def edecrypt_(mode,inputfilepath):
    if mode == 'encrypt':
        inputfilename = os.path.basename(inputfilepath)
        outputfilename = inputfilename[:inputfilename.rfind('.')]+'.enc'+inputfilename[inputfilename.rfind('.'):]
        outputfilepath = os.path.join(os.path.dirname(inputfilepath),outputfilename)

        with open(inputfilepath, 'rb') as in_file, open(outputfilepath, 'wb') as out_file:
            encrypt(in_file, out_file, password)
    elif mode == 'decrypt':
        inputfilename = os.path.basename(inputfilepath)
        outputfilename = inputfilename.replace('.enc','')
        outputfilepath = os.path.join(os.path.dirname(inputfilepath),outputfilename)

        with open(inputfilepath, 'rb') as in_file, open(outputfilepath, 'wb') as out_file:
            decrypt(in_file, out_file, password)
    return outputfilepath