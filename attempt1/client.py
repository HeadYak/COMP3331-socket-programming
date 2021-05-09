import sys
from socket import *               # Import socket module


# python client.py server_IP server_port client_udp_server_port


client_socket = socket(AF_INET, SOCK_STREAM)     # Create a socket object
host = sys.argv[1]                   # Get host
port = int(sys.argv[2])              # Reserve a port for your service.

client_socket.connect((host, port))


sockets_list = [client_socket]


username = input("Username: ").strip()
password = input("Password: ").strip()

login = username + ' ' + password

login = login.encode('utf-8')
client_socket.sendall(login)

loggedin = False

while True:
    max_reattempts = client_socket.recv(1024).decode('utf-8')

    reattempt = 0
    if loggedin != True:
        login_resp = client_socket.recv(1024).decode('utf-8')
        while(True):
            if loggedin == True:
                break
            # login_resp = client_socket.recv(1024).decode('utf-8')
            if 'Welcome' in login_resp:
                print(login_resp)
                loggedin = True
                sockets_list.append(client_socket)





                # print(sockets_list)
            elif 'Invalid login. Please retry' in login_resp:
                print("Max reattempts:", max_reattempts)
                reattempt = reattempt + 1
                print(login_resp, reattempt)
                username = input("Username: ").strip()
                password = input("Password: ").strip()

                login = username + ' ' + password
                login = login.encode('utf-8')
                client_socket.sendall(login)
                client_socket.close()                     # Close the socket when done
        command = input("Enter one of the following commands(MSG, DLT, EDT, RDM, ATU,OUT): ").strip()

#Welcome

client_socket.close()                     # Close the socket when done
