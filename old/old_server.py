#coding: utf-8
# pylint: disable-all


import sys

from socket import *


if(len(sys.argv) != 3):
    print("Usage: python3 server.py server_port number_of_consecutive_failed_attempts")
    quit()

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
max_attempts = sys.argv[2]
# python server.py server_port number_of_consecutive_failed_attempts
print("Server running on ", str(HOST)+":"+str(PORT))


server_socket = socket(AF_INET, SOCK_STREAM)


server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

client_socket, client_address = server_socket.accept()

print('Connected by', client_address)


data = client_socket.recv(1024)

print(data)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             decode = data.decode()
#             print(decode)
#             # if not data:
#             #     break
#             conn.sendall(data)
