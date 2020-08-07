import socket
import threading

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = int(input("Port number for hosting: "))
ThreadCount = 0
ServerSocket.bind((host, port))
print("Waiting for a Connection..")
ServerSocket.listen(5)

def threaded_client(connection):
    connection.send(str.encode("Welcome to the Server\n"))
    while True:
        data = connection.recv(2048)
        if not data:
            break
        msg_all_clients(data.decode("utf-8"))
    connection.close()

def msg_all_clients(msg):
    global clients
    for client in clients:
        try:
            client.sendall(str.encode(msg))
        except:
            print("could not send data to {0} it is likely they are no longer present on the network".format(client))
clients = []

while True:
    Client, address = ServerSocket.accept()
    threading._start_new_thread(threaded_client, (Client, ))
    clients.append(Client)
    ThreadCount += 1
    print("Connected to: {0} : {1}".format(address[0], address[1]))
    print("Thread Number: {0}".format(ThreadCount))
    print("Clients:\n", clients)
    msg_all_clients("New client has connected")

ServerSocket.close()