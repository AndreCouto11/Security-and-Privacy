from dataclasses import dataclass
from multiprocessing.connection import Client
import socket
import time
import random
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
import pandas as pd
from Crypto.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Crypto import Random

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serverSocket.bind(("127.0.0.1",9090))
serverSocket.listen()
(clientConnected,ClientAddress) = serverSocket.accept()
print("Accept connection from %s:%s"%(ClientAddress[0],ClientAddress[1]))


server_string = clientConnected.recv(1024)
server_public_key = RSA.importKey(server_string)

cipher = PKCS1_OAEP.new(server_public_key)

AESkey = get_random_bytes(16)

ciphertext = cipher.encrypt(AESkey)
clientConnected.send(ciphertext)

time.sleep(3)
start = time.process_time()
file_in = open("encryptedfile.bin", "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]

cipher = AES.new(AESkey, AES.MODE_EAX, nonce)
#data = cipher.decrypt_and_verify(ciphertext, tag) #com verificaçao
data = cipher.decrypt(ciphertext)                   #sem verificaçao
with open('decrypted.csv','w') as decrypted_file:
    decrypted_file.write(data.decode('UTF-8'))

finish = time.process_time()
print("TIME: ",finish-start)
data = pd.read_csv("decrypted.csv")

print(data.columns)

df = data.loc[data.infringed==1]

dg = df.filter(['infringed','past_avg_amount_annuity','past_avg_amt_application','past_avg_amt_credit','past_loans_approved','past_loans_refused','past_loans_canceled','past_loans_unused','past_loans_total'])

dg.to_csv('infriged.csv')


dt = df.filter(['infringed','gender','age','num_children'])

dt.to_csv('age.csv')








