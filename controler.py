from Crypto.Cipher import AES
from email import message
from http import server
import socket
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import pandas as pd
from Crypto import Random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import time


clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


clientsocket.connect(("127.0.0.1",9090))

random_generator = Random.new().read
private_key = RSA.generate(4080, random_generator)
public_key = private_key.publickey()

clientsocket.send(public_key.export_key())


with open('infringement_dataset.csv','rb') as file:
    original = file.read()

start = time.process_time()
decryptor =  PKCS1_OAEP.new(private_key)
keyEncript = clientsocket.recv(1024)
key = decryptor.decrypt(keyEncript)

cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(original)

file_out = open("encryptedfile.bin", "wb")
[ file_out.write(x) for x in (cipher.nonce, tag, ciphertext) ]
file_out.close()
finish = time.process_time()

print("Time: ",finish-start)





