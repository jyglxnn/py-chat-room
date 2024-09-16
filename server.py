# threading is a sequence of instruction within the program
# multi-threading run an invidual thread for each client as to handle the threads in the same time 
import threading
import socket 

# predefined host IP and port
host = '127.0.0.1'
port = 62600

# initiate server object socket.AF_INET(address family IPv4) socket.SOCK_STREAM(connection oriented TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

clients = []
aliases = []

# broadcast() message from server to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)

# handle_client() handling client to send to other client
def handle_client(client):
    while True:
        try: 
            # recieve the client itself message 1024 bytes maximum bytes server can receive from client 
            message = client.recv(1024)
            # broadcast message 
            broadcast(message)
        # is client is have a error
        except:
            # to check the client to get the index in clients list
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast('{} left the room'.format(alias).encode('utf-8'))
            aliases.remove(alias)
            break

# receive() receiving client
def receive():
    while True:
        print('Server is running...')
        
        client, address = server.accept()
        print('Connection established {}'.format(str(address)))
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print('user set name {}'.format(alias).encode('utf-8'))
        broadcast(f'{alias} connected in the room'.encode('utf-8'))
        client.send('[!] you are now connected'.encode('utf-8'))
        
        thread = threading.Thread(target = handle_client, args = (client,))
        thread.start()

if __name__ == "__main__":
    receive()
