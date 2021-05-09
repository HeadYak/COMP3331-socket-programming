from socket import *
import sys


# if(len(sys.argv) != 3):

#     print("python client.py server_IP server_port client_udp_server_port")
#     quit()


HOST = sys.argv[1]  # The server's hostname or IP address
PORT = int(sys.argv[2])        # The port used by the server


client_socket = socket(AF_INET, SOCK_STREAM)

# Connect to a given server_name and server_port
client_socket.connect((HOST, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)


username = input("Username: ")
password = input("Password: ")

login = username + ' ' + password
client_socket.connect((HOST, PORT))
packet = str.encode(login)
client_socket.sendall(packet)





client_socket.close()


# client_socket.send(user_header + credentials)


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

#     username = input("Username: ")
#     password = input("Password: ")

#     login = username + ' ' + password
#     s.connect((HOST, PORT))
#     packet = str.encode(login)
#     s.sendall(packet)
#     data = s.recv(1024)

# print('Received', repr(data))
