import socket
import threading
import pickle
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
###############################################################################
#receives data from server and prints on screen
def receive():
    while True:
        msg = ClientSocket.recv(2048)
        msg = f.decrypt(msg)
        msg = msg.decode("utf-8")
        print(msg)
###############################################################################
#input for host ip, port and user's username
host = input("Enter server IP: ")
port = int(input("Enter server port: "))
username = input("Username: ")
key = input("Enter encryption key: ")
key = bytes(key, "utf-8")
#setup connection to host
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting to connect")
ClientSocket.connect((host, port))
print("Connected")
###############################################################################
#set up encryption:
salt = b'D;\x94\xf8\xd1\x1baV\x91m\n\xb0E\x04E\xa0' #make this not hard coded later!!!!
kdf = PBKDF2HMAC(
     algorithm=hashes.SHA256(),
     length=32,
     salt=salt,
     iterations=100000,
     backend=default_backend()
 )
key = base64.urlsafe_b64encode(kdf.derive(key))
print("key: ", key)
f = Fernet(key)
#receive files from server upon connection:
#this code is for accepting the log file from the server, which is supplied on joining
HEADERSIZE = 10
full_msg = b''
new_msg = True
while True:
    msg = ClientSocket.recv(16)
    if new_msg:
        msglen = int(msg[:HEADERSIZE])
        new_msg = False
    full_msg += msg
    if len(full_msg)-HEADERSIZE == msglen:
        logs = pickle.loads(full_msg[HEADERSIZE:])
        break
#print logs to terminal:
for i in logs:
    i = bytes(i, "utf-8")
    i = f.decrypt(i)
    print(i.decode("utf-8"))

#normal message send/receive:
#receive thread to get messages without being blocked
threading._start_new_thread(receive, ())
#this loop gets user input and sends it to the server with the username appended
while True:
    Input = input()
    msg = "{0} said: {1} \n".format(username,Input)
    msg = f.encrypt(bytes(msg, "utf-8"))
    ClientSocket.send(msg)
ClientSocket.close()
