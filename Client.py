import socket
import threading
import pickle
from encodedecode import encode
from encodedecode import decode 
###############################################################################
#receives data from server and prints on screen
def receive(key):
    while True:
        msg = ClientSocket.recv(2048)      
        msg = msg.decode("utf-8")
        msg = decode(key, msg)
        print(msg)
###############################################################################
#input for host ip, port and user's username
host = input("Enter server IP: ")
port = int(input("Enter server port: "))
username = input("Username: ")
key = input("Enter obscurity key: ")
#setup connection to host 
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Attempting to connect")
ClientSocket.connect((host, port))
print("Connected")
###############################################################################

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
    print(decode(key, i))

#normal message send/receive:
#receive thread to get messages without being blocked
threading._start_new_thread(receive, (key, ))
#this loop gets user input and sends it to the server with the username appended
while True:
    Input = input()
    msg = "{0} said: {1} \n".format(username,Input)
    msg = encode(key, msg)
    ClientSocket.send(str.encode(msg))
ClientSocket.close()