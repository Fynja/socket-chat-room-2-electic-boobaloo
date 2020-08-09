import socket
import threading
import pickle
import base64
import os
import time
import tkinter as tk
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
###############################################################################
#receives data from server, decrypts it, and prints on screen
def receive():
    while True:
        msg = ClientSocket.recv(2048)
        try:
            msg = f.decrypt(msg)
            msg = msg.decode("utf-8")
            print(msg)
        except:
            print("Failed to a decrypt message.")
###############################################################################
#takes input from tkinter entry widgit then encrypts and sends to server
def send(e):
    global trustkey
    if trustkey == True: #if someone accidentally enters the wrong passwod and/or salt then it will be detected and they will be asked not to send messages to the server
        Input = e.widget.get()
        msg = "{0} said: {1} \n".format(username,Input)
        msg = f.encrypt(bytes(msg, "utf-8"))
        ClientSocket.send(msg)
        e.widget.delete(0, tk.END)
    else:
        print("It was detected that you had an error decrypting a message from this server.")
        print("For this reason you cannot send any messages to the server to prevent it being flooded with gibberish.")
        print("Restart your client and check your password and salt.")
        time.sleep(60)
        exit()
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
try:
    ClientSocket.connect((host, port))
    print("Connected")
except Exception as e:
    print("Could not connect to server for the following reason:")
    print(e)
    time.sleep(60)
    exit()
trustkey = True #will be switched to false if any errors with decryption are detected during the reading of logs, this is to prevent a user accidentally filling a servers log with messages that use the wrong key
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
print(key.decode("utf-8")) #print key (this is not a great idea, but considering the user enters the password and salt as plaintext its not going to make much of a difference if someone is spying on their screen)
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
        print("Failed to decrypt a message.")
        trustkey = False
    print(i.decode("utf-8"))

window = tk.Tk()
label = tk.Label(text="Send message:")
entry = tk.Entry(width=256)
threading._start_new_thread(receive, ())
label.pack()
entry.pack()
entry.bind("<Return>", send)
text = entry.get()
window.mainloop()
ClientSocket.close()
