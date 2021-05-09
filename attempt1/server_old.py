import sys

from socket import *

# python server.py server_port number_of_consecutive_failed_attempts

s = socket()         # Create a socket object
# host = gethostname()  # Get local machine name
host = '127.0.0.1'  # Get local machine name
port = int(sys.argv[1])            # Reserve a port for your service.
maxattempts = int(sys.argv[2])

s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.


clients = []


print("Server running on", str(host)+":"+str(port))
count = 0
while True:
    login_match = False
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)



    data = c.recv(1024).decode('utf-8')

    firstname = data.split()[0]



    c.sendall(b'Thank you for connecting')

    login_file = open("credentials.txt", "r")
    for line in login_file:
        stripped_line = line.strip()
        # print(stripped_line)
        if(stripped_line == data):
            login_match = True

    if(login_match == True):
        welcomemsg = "Welcome " + firstname
        welcomemsg = welcomemsg.encode('utf-8')
        c.sendall(welcomemsg)

        if clients == []:
            client = {
                'addr': addr,
                'failed_attempts': 0
            }
            client_copy = client.copy()
            clients.append(client_copy)

        else:
            found = False
            for client in clients:
                if client['addr'] == addr:
                    found = True
            if found == False:
                client = {
                    'addr': addr,
                    'failed_attempts': 0
                }
                client_copy = client.copy()
                clients.append(client_copy)
    elif login_match == False:
        if clients == []:
            client = {
                'addr': addr,
                'failed_attempts': 1
            }
            client_copy = client.copy()
            clients.append(client_copy)
        else:
            found = False
            for client in clients:
                if client['addr'] == addr:
                    found = True
            if found == False:
                client = {
                    'addr': addr,
                    'failed_attempts': client['failed_attempts'] + 1
                }
                client_copy = client.copy()
                clients.append(client_copy)

    print(clients)

    c.close()                # Close the connection
