import sys

from socket import *

# python server.py server_port number_of_consecutive_failed_attempts

server_socket = socket(AF_INET, SOCK_STREAM)         # Create a socket object
# host = gethostname()  # Get local machine name
host = '127.0.0.1'  # Get local machine name
port = int(sys.argv[1])            # Reserve a port for your service.
max_reattempts = int(sys.argv[2])

server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


server_socket.bind((host, port))        # Bind to the port

server_socket.listen()                 # Now wait for client connection.


clients = []


print("Server running on", str(host)+":"+str(port))
while 1:
    print("Yoyo")
    login_match = False

    client_socket, client_addr = server_socket.accept()     # Establish connection with client.


    max_reattempt_msg = repr(max_reattempts).encode('utf-8')
    client_socket.sendall(max_reattempt_msg)

    print('Got connection from', client_addr)


    data = client_socket.recv(1024).decode('utf-8')

    username = data.split()[0]
    password = data.split()[1]

    print(data)

    login_file = open("credentials.txt", "r")
    for line in login_file:
        stripped_line = line.strip()
        stored_username = stripped_line.split()[0]
        stored_password = stripped_line.split()[1]
        # print(stripped_line)
        if(stripped_line == data):
            login_match = True
            print("Valid login provided by ", client_addr)
        elif(username == stored_username and password != stored_password):
            print("Correct username but incorrect provided by ", client_addr)

    if(login_match == True):
        welcomemsg = "Welcome " + username
        welcomemsg = welcomemsg.encode('utf-8')
        client_socket.sendall(welcomemsg)

    elif(login_match == False):
        errormsg = "Invalid login. Please retry"
        errormsg = errormsg.encode('utf-8')
        client_socket.sendall(errormsg)

    login_file.close()



client_socket.close()                # Close the connection
server_socket.close()
