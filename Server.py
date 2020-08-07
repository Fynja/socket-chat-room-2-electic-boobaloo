import socket
import threading
###############################################################################
#when a new connection is established this function is run on a new thread
#it waits for information to be received from a client then calls msg_all_clients to pass that information to other clients
def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        if not data:
            break
        msg_all_clients(data.decode("utf-8"))
    connection.close()
###############################################################################
#reads through clients list and sends a message to each client
#will also remove any clients it was unable to send a message to
def msg_all_clients(msg):
    global clients
    for clientID in range(len(clients)):
        try:
            clients[clientID].sendall(str.encode(msg))
        except:
            print("could not send data to {0} it is likely they are no longer present on the network".format(clients[clientID]))
            print("removing problematic client")
            clients.pop(clientID)
###############################################################################
#set up server:
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = int(input("Port number for hosting: "))
ServerSocket.bind((host, port))
#listen for a connection:
print("Waiting for a Connection..")
ServerSocket.listen(5)
#define some variables
clients = []
ThreadCount = 0
while True:
    #accept new connection and create thread for new client:
    Client, address = ServerSocket.accept()
    threading._start_new_thread(threaded_client, (Client, ))
    #adjust variables:
    clients.append(Client)
    ThreadCount += 1
    #print information to console:
    print("Connected to: {0} : {1}".format(address[0], address[1]))
    print("Thread Number: {0}".format(ThreadCount))
    print("Clients:\n", clients)
    #message all clients saying a new client has connected:

ServerSocket.close()