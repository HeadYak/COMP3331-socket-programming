import sys
import threading
from socket import *
from time import*
# python server.py server_port number_of_consecutive_failed_attempts

server_socket = socket(AF_INET, SOCK_STREAM)         # Create a socket object
# host = gethostname()  # Get local machine name
host = '127.0.0.1'  # Get local machine name
port = int(sys.argv[1])            # Reserve a port for your service.

open("userlog.txt", "w")

max_reattempts = int(sys.argv[2])

block_time = 10

server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


server_socket.bind((host, port))        # Bind to the port

server_socket.listen()                 # Now wait for client connection.

failed_auths = []
block_accs = []
print("Server running on", str(host)+":"+str(port))


#Threading function to check if any acc is to be unblocked
def unblock():
    threading.Timer(1.0, unblock).start()
    if(block_accs != []):
        timenow = int(time())
        for block_acc in list(block_accs):
            if block_acc['blocktil'] < timenow:
                print(block_acc['username'], "unblocked")
                block_accs.remove(block_acc)
                # print(block_accs)



    # print("block_accs", block_accs)





while 1:
    unblock()

    client_socket, client_addr = server_socket.accept()
    print("Connection from:",client_addr)

    loggedin = False


    while(loggedin == False):
        print("Blocked accs:")
        print(block_accs)


        if(failed_auths != []):
            for failed_auth in list(failed_auths):

                #Block user if they exceed maximum reattempts
                if failed_auth['failed_auth_attempts'] == max_reattempts:
                    timenow = int(time())
                    blocktil = timenow + 10
                    block_acc = {
                        'username': failed_auth['username'],
                        'blocktil': blocktil
                    }
                    block_acc_copy = block_acc.copy()
                    block_accs.append(block_acc_copy)

                    # print("Blocked accounts")
                    # print(block_accs)
                    failed_auths.remove(failed_auth)

        #Receive username and password from client
        login_data = client_socket.recv(1024).decode('utf-8')
        print("Input from", client_addr,":",login_data)

        username = login_data.split()[0]
        password = login_data.split()[1]
        print("Input username:",username)
        print("Input password:",password)

        login_file = open("credentials.txt", "r")




        username_match = False
        password_match = False
        total_match = False
        acc_blocked = False


        for block_acc in list(block_accs):

            if ((block_acc['username'] == username) and
                (block_acc['blocktil'] > timenow)):
                acc_blocked = True
                print("Account", username,"blocked")

        # print("Middle of loop")
        # print(block_accs)

        for line in login_file:
            stripped_line = line.strip()
            stored_username = stripped_line.split()[0]
            stored_password = stripped_line.split()[1]
            if(stored_username == username and
                stored_password == password):
                print("Valid login provided by", client_addr)
                total_match = True
            elif(stored_username == username and
                stored_password != password):
                print("Valid username but incorrect password by", client_addr)
                username_match = True

        if(acc_blocked == True):
            blockmsg = "Account blocked due to too many failed attempts. Please try again later"
            blockmsg = blockmsg.encode('utf-8')
            client_socket.sendall(blockmsg)

        elif(total_match == True):
            welcomemsg = "Welcome " + username
            welcomemsg = welcomemsg.encode('utf-8')
            client_socket.sendall(welcomemsg)
            loggedin = True
        elif(username_match == True and password_match == False):
            passworderrormsg = "Invalid password. Please Try again"
            passworderrormsg = passworderrormsg.encode('utf-8')
            client_socket.sendall(passworderrormsg)

            if(failed_auths == []):
                failed_auth = {
                    'username': username,
                    'failed_auth_attempts': 1
                }
                failed_auth_copy = failed_auth.copy()
                failed_auths.append(failed_auth_copy)
            else:
                failed_before = False
                for failed_auth in failed_auths:
                    if(failed_auth['username'] == username):
                        failed_auth['failed_auth_attempts'] = failed_auth['failed_auth_attempts'] + 1
                        failed_before = True

                if(failed_before == False):
                    failed_auth = {
                        'username': username,
                        'failed_auth_attempts': 1
                    }
                    failed_auth_copy = failed_auth.copy()
                    failed_auths.append(failed_auth_copy)
            # print(failed_auths)

        elif(username_match == False and password_match == False):
            loginerrormsg = "Invalid login. Please Try again"
            loginerrormsg = loginerrormsg.encode('utf-8')
            client_socket.sendall(loginerrormsg)

    print("YOYO")
    with open('userlog.txt', "r+") as logf:
        lines = logf.readlines()

        if lines == []:
            count = 1
            ctimenow = ctime(time())

            logf_string = str(count)+"; "+str(ctimenow)+"; "+username+"; "+client_addr[0]
            print(logf_string)
            logf.write(logf_string+"\n")

        elif lines[-1] != "":
            ctimenow = ctime(time())
            split_line = lines[-1].split(';')
            count = int(split_line[0]) + 1
            logf_string = str(count)+"; "+str(ctimenow)+"; "+username+"; "+client_addr[0]
            logf.write(logf_string+"\n")

    while(loggedin == True):
        input_command = client_socket.recv(1024).decode('utf-8')
        print(input_command, username)

