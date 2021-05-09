import sys
from socket import *               # Import socket module


# python client.py server_IP server_port client_udp_server_port


client_socket = socket(AF_INET, SOCK_STREAM)     # Create a socket object
sockets_list = [client_socket]
host = sys.argv[1]                   # Get host
port = int(sys.argv[2])              # Reserve a port for your service.
udp_port = int(sys.argv[3])
client_socket.connect((host, port))
print("Connection OK")
# client_socket.setblocking(False)

# client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

loggedin = False
while(True):
    while(loggedin == False):
        # print(loggedin)
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        login = username + ' ' + password + ' ' + str(udp_port)

        login = login.encode('utf-8')
        client_socket.sendall(login)
        login_resp = client_socket.recv(1024).decode('utf-8')

        print(login_resp)

        #If welcome message received set user as loggedin
        if login_resp == "Welcome " + username:
            loggedin = True
            # break

    while(loggedin == True):
        user_command = input(
            "Enter one of the following commands(MSG, DLT, EDT, RDM, ATU, OUT, UPD): ")
        user_command = user_command.encode('utf-8')
        client_socket.sendall(user_command)
        resp = client_socket.recv(1024).decode('utf-8')
        print(resp)

        #If logout message receive set user as logged out
        if resp == 'User logged out successfully':
            loggedin = False
    # break






