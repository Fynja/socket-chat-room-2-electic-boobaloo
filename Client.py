import socket
import threading
###############################################################################
#receives data from server and prints on screen
def receive():
    while True:
        msg = ClientSocket.recv(1024)      
        print("\n", msg.decode("utf-8"))
###############################################################################
#input for host ip, port and user's username
host = input("Enter server IP: ")
port = int(input("Enter server port: "))
USRN = input("Username: ")
#setup connection to host 
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Attempting to connect')
ClientSocket.connect((host, port))
###############################################################################
#receive thread to get messages without being blocked
threading._start_new_thread(receive, ())
#this loop gets user input and sends it to the server with the username appended
while True:
    Input = input()
    msg = "{0} said: {1}".format(USRN,Input)
    ClientSocket.send(str.encode(msg))
ClientSocket.close()