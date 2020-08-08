import socket
import threading
import pickle
import base64
import os
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
###############################################################################
#receives data from server and prints on screen
def receive():
    while True:
        msg = ClientSocket.recv(2048)
        try:
            msg = f.decrypt(msg)
            msg = msg.decode("utf-8")
            print(msg)
        except:
            print("failed to a decrypt message!")
            print("either you have the wrong password and/or salt, or someone else is messaging using the wrong password and/or salt")

###############################################################################
#set up all the required user defined variables:
host = input("Enter server IP: ")
port = int(input("Enter server port: "))
username = input("Username: ")
password = input("Enter encryption password: ")
password = bytes(password, "utf-8")
salt = input("Enter salt: ")
salt = bytes(salt, "utf-8")
#setup connection to host
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting to connect")
ClientSocket.connect((host, port))
print("Connected")
trustkey = True #will be switched to false if any errors with decryption are detected, this is to prevent a user accidentally filling a servers log with messages that use the wrong key
###############################################################################
#set up encryption:
kdf = PBKDF2HMAC(
     algorithm=hashes.SHA256(),
     length=32,
     salt=salt,
     iterations=100000,
     backend=default_backend()
 )
key = base64.urlsafe_b64encode(kdf.derive(password))
print("{0}**********************************".format(key[:10].decode("utf-8")))
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
    try:
        i = f.decrypt(i)
    except:
        print("DECRYPTION OF A MESSAGE FAILED!")
        trustkey = False
    print(i.decode("utf-8"))


#normal message send/receive:
#receive thread to get messages without being blocked
threading._start_new_thread(receive, ())
#this loop gets user input and sends it to the server with the username appended
while True:
    if trustkey == True:
        Input = input()
        msg = "{0} said: {1} \n".format(username,Input)
        msg = f.encrypt(bytes(msg, "utf-8"))
        ClientSocket.send(msg)
    else:
        print("It was detected that you had an error decrypting a message from this server")
        print("for this reason you cannot send any messages to the server to prevent it being flooded with gibberish")
        print("restart your client and check your password and salt")
        time.sleep(6000)
ClientSocket.close()
