import socket
import threading
import time
import pickle
###############################################################################
#when a new connection is established this function is run on a new thread
#it waits for information to be received from a client then calls msg_all_clients to pass that information to other clients
def threaded_client(connection, log):
    #send log file to client upon connection
    file = pickle.dumps(log)
    HEADERSIZE = 10
    file = bytes(f'{len(file):<{HEADERSIZE}}', "utf-8") + file
    connection.send(file)
    #normal messaging:
    while True:
        try:
            data = connection.recv(2048)
            log.append(data.decode("utf-8"))
        except Exception as e:
            print(e)
            exit()
        if not data:
            break
        msg_all_clients(data.decode("utf-8"))
    connection.close()
###############################################################################
#reads through clients list and sends a message to each client
#will also remove any clients it was unable to send a message to
def msg_all_clients(msg):
    global clients
    clientID = 0
    while clientID < len(clients):
        try:
            clients[clientID].send(str.encode(msg))
        except Exception as e:
            print("===================================")
            print("Could not send data to clientID {0} it is likely they are no longer present on the network".format(clientID))
            print("Exception Info: ", e)
            try:
                print("Attempting to remove problematic client information")
                clients.pop(clientID)
                print("Client information removed")
                clientID -= 1
            except Exception as e:
                print("Could not remove client information for the following reason:")
                print(e)
            print("===================================")
        clientID += 1
###############################################################################
#saves message history to server.log
def savelog(log):
    x = 10
    print("Log will be saved to file every {0} seconds".format(x))
    while True:
        with open("Server.log", 'wb') as f:
            pickle.dump(log, f)
        time.sleep(x)
###############################################################################
#set up server:
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = int(input("Port number for hosting: "))
ServerSocket.bind((host, port))
try:
    with open('Server.log','rb') as f:
        log = pickle.load(f)
except:
    print("Log file not found, a new one will be created")
    log = []
threading._start_new_thread(savelog, (log, ))
#listen for a connection:
print("Waiting for a Connection..")
ServerSocket.listen(5)
#define some variables
clients = []
ThreadCount = 0
while True:
    #accept new connection and create thread for new client:
    Client, address = ServerSocket.accept()
    threading._start_new_thread(threaded_client, (Client, log))
    #adjust variables:
    clients.append(Client)
    ThreadCount += 1
    #print information to console:
    print("New connection from: {0} : {1}".format(address[0], address[1]))
    print("Thread Number: {0}".format(ThreadCount))
    print("Clients:")
    for c in clients:
        print(c)
    print("===================================")
ServerSocket.close()
