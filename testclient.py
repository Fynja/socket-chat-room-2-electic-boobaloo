import socket
import threading

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input("Enter server IP: ")
port = int(input("Enter server port: "))
print('Attempting to connect')
ClientSocket.connect((host, port))
Response = ClientSocket.recv(1024)
USRN = input("Username: ")

def receive():
    while True:
        msg = ClientSocket.recv(1024)      
        print("\n", msg.decode("utf-8"))
threading._start_new_thread(receive, ())

while True:
    Input = input()
    msg = "{0} said: {1}".format(USRN,Input)
    ClientSocket.send(str.encode(msg))
ClientSocket.close()
