import socket
import threading

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 25565
print('Attempting to connect')
ClientSocket.connect((host, port))
Response = ClientSocket.recv(1024)

def receive():
    while True:
        msg = ClientSocket.recv(1024)      
        print("\nServer says: ", msg.decode("utf-8"))
threading._start_new_thread(receive, ())

while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
ClientSocket.close()
