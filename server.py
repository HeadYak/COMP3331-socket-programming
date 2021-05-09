import sys
import threading
from socket import *
from time import*
from _thread import *
# python server.py server_port number_of_consecutive_failed_attempts

server_socket = socket(AF_INET, SOCK_STREAM)         # Create a socket object
# host = gethostname()  # Get local machine name
host = '127.0.0.1'  # Get local machine name
port = int(sys.argv[1])            # Reserve a port for your service.

open("userlog.txt", "w")
open("messagelog.txt", "w")


max_reattempts = int(sys.argv[2])

block_time = 10

server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


server_socket.bind((host, port))        # Bind to the port

server_socket.listen()                 # Now wait for client connection.

failed_auths = []
block_accs = []
print("Server running on", str(host)+":"+str(port))


def threaded_client(connection):


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
        login_data = connection.recv(1024).decode('utf-8')
        print("Input from", client_addr, ":", login_data)

        #Extract input from client
        username = login_data.split()[0]
        password = login_data.split()[1]
        udp_port = login_data.split()[2]
        print("Input username:", username)
        print("Input password:", password)

        login_file = open("credentials.txt", "r")

        username_match = False
        password_match = False
        total_match = False
        acc_blocked = False

        #Code below checks if an account is blocked
        for block_acc in list(block_accs):

            if ((block_acc['username'] == username) and
                    (block_acc['blocktil'] > timenow)):
                acc_blocked = True
                print("Account", username, "blocked")

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
            connection.sendall(blockmsg)

        elif(total_match == True):
            welcomemsg = "Welcome " + username
            welcomemsg = welcomemsg.encode('utf-8')
            connection.sendall(welcomemsg)
            loggedin = True
        elif(username_match == True and password_match == False):
            passworderrormsg = "Invalid password. Please Try again"
            passworderrormsg = passworderrormsg.encode('utf-8')
            connection.sendall(passworderrormsg)

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
            connection.sendall(loginerrormsg)

    #Write user details into userlog
    with open('userlog.txt', "r+") as logf:
        lines = logf.readlines()

        if lines == []:
            count = 1
            ctimenow = ctime(time())

            logf_string = str(count)+"; "+str(ctimenow)+ \
                "; "+username+"; "+client_addr[0]+"; "+udp_port
            # print(logf_string)
            logf.write(logf_string+"\n")

        elif lines[-1] != "":
            ctimenow = ctime(time())
            split_line = lines[-1].split(';')
            count = int(split_line[0]) + 1
            logf_string = str(count)+"; "+str(ctimenow)+ \
                "; "+username+"; "+client_addr[0]+"; "+udp_port
            logf.write(logf_string+"\n")

    while(loggedin == True):
        userinputs = connection.recv(1024).decode('utf-8').split()
        user_command = userinputs[0]
        print(user_command,"executed by", username)

        #Loop for MSG command
        if(user_command == "MSG"):
            message = userinputs[1:]
            message_str = ' '.join(word for word in message)
            with open('messagelog.txt', "r+") as messagef:
                lines = messagef.readlines()

                if lines == []:
                    count = 1
                    ctimenow = ctime(time())

                    messagef_string = str(count)+"; "+str(ctimenow) + \
                        "; "+username+"; "+message_str+"; "+'False'
                    # print(logf_string)
                    messagef.write(messagef_string+"\n")

                elif lines[-1] != "":
                    ctimenow = ctime(time())
                    split_line = lines[-1].split(';')
                    count = int(split_line[0]) + 1
                    messagef_string = str(count)+"; "+str(ctimenow) + \
                        "; "+username+"; "+message_str+"; "+'False'
                    # print(logf_string)
                    messagef.write(messagef_string+"\n")

            send_string = "Message sent successfully"
            send_string = send_string.encode('utf-8')
            connection.sendall(send_string)

        #Loop for RDM command
        elif(user_command == "RDM"):

            #Accept epoch timestamp only
            timestampinput = userinputs[1]

            with open('messagelog.txt', "r+") as messagef:
                lines = messagef.readlines()

                # print(lines)
                read_string = "Messages before timestamp:\n"

                #Case if messagelog.txt is empty
                if lines == []:
                    read_string = "No message history"
                    read_string = read_string.encode('utf-8')
                    connection.sendall(read_string)

                #Case if messagelog.txt is not empty
                elif lines != []:
                    for line in lines:
                        line_split = line.split(';')
                        temp = line_split[1].strip()
                        pattern = '%a %b %d %H:%M:%S %Y'
                        epoch = int(mktime(strptime(temp, pattern)))
                        if epoch > int(timestampinput):
                            read_string = read_string + line

                    read_string = read_string.strip()
                    read_string = read_string.encode('utf-8')
                    connection.sendall(read_string)

        #Loop for EDT command
        elif(user_command == "EDT"):
            edited = False
            messagenumber = userinputs[1]
            timestamp = userinputs[2]
            message_edit = userinputs[3:]
            message_edit = ' '.join(word for word in message_edit)
            with open('messagelog.txt', "r+") as messagef:
                lines = messagef.readlines()

                if lines == []:
                    edit_string = "No message history"
                    edit_string = edit_string.encode('utf-8')
                    connection.sendall(edit_string)
                elif lines != []:
                    temp = []
                    for line in lines:
                        ctimenow = ctime(time())
                        line_split = line.split(';')
                        stored_number = line_split[0]
                        stored_number = stored_number.strip()
                        stored_user = line_split[2]
                        stored_user = stored_user.strip()
                        stored_time = line_split[1]
                        stored_time = stored_time.strip()

                        pattern = '%a %b %d %H:%M:%S %Y'
                        epoch = int(mktime(strptime(stored_time, pattern)))
                        if username == stored_user and messagenumber == stored_number and (epoch == timestamp or timestamp == 'timestamp'):

                            count = int(line_split[0])
                            editf_string = str(count)+"; "+str(ctimenow) + \
                                "; "+username+"; "+str(message_edit)+"; "+'True'
                            line = editf_string
                            print("Edit: "+editf_string)
                            edited = True
                        temp.append(line)
                        # print(temp)
                    with open('messagelog.txt', 'w') as messagef:
                        messagef.writelines(temp)

                        if edited == True:
                            edit_string = "Message edited successfully"
                        else:
                            edit_string = "Unable to edit message"
                        edit_string = edit_string.encode('utf-8')
                        connection.sendall(edit_string)
        #Loop for DLT command
        elif(user_command == "DLT"):
            deleted = False
            messagenumber = userinputs[1]
            timestamp = userinputs[2]

            with open('messagelog.txt', "r+") as messagef:
                temp = []
                lines = messagef.readlines()

                #Case if messagelog is empty
                if lines == []:
                    delete_string = "No message history"
                    delete_string = edit_string.encode('utf-8')
                    connection.sendall(delete_string)

                #Case if messagelog is not empty
                elif lines != []:
                    count = 1
                    for line in lines:

                        line_split = line.split(';')
                        stored_number = line_split[0]
                        stored_number = stored_number.strip()
                        stored_user = line_split[2]
                        stored_user = stored_user.strip()
                        stored_time = line_split[1]
                        stored_time = stored_time.strip()
                        stored_message = line_split[3]
                        stored_message = stored_message.strip()
                        pattern = '%a %b %d %H:%M:%S %Y'
                        epoch = int(mktime(strptime(stored_time, pattern)))
                        if username == stored_user and messagenumber == stored_number and (epoch == timestamp or timestamp == 'timestamp'):
                            delete_string = "Message deleted successfully"
                            delete_string = delete_string.encode('utf-8')
                            connection.sendall(delete_string)
                            deleted = True
                        else:
                            shift_string = str(count)+"; "+str(stored_time) + \
                                "; "+str(stored_user)+"; " + \
                                str(stored_message)+"; "+'False'
                            count = count + 1

                            # print(shift_string)
                            temp.append(shift_string)

                    with open('messagelog.txt', 'w') as messagef:
                        messagef.writelines(temp)
            if deleted == False:
                delete_string = "Message could not be deleted"
                delete_string = delete_string.encode('utf-8')
                connection.sendall(delete_string)
        #Loop for OUT command
        elif(user_command == 'OUT'):
            with open('userlog.txt', "r+") as userf:
                temp = []
                lines = userf.readlines()
                if lines != []:
                    count = 1
                    for line in lines:
                        line_split = line.split(';')
                        stored_number = line_split[0]
                        stored_number = stored_number.strip()
                        stored_time = line_split[1]
                        stored_time = stored_time.strip()
                        stored_user = line_split[2]
                        stored_user = stored_user.strip()
                        stored_addr = line_split[3]
                        stored_addr = stored_addr.strip()
                        stored_udp = line_split[4]
                        stored_udp = stored_udp.strip()
                        if username == stored_user:
                            logout_string = "User logged out successfully"
                            logout_string = logout_string.encode('utf-8')
                            connection.sendall(logout_string)
                            loggedin = False
                        else:
                            logout_string = str(count)+"; "+str(stored_time) + \
                                "; "+str(stored_user)+"; " + \
                                str(stored_addr)+"; "+str(stored_udp)
                            count = count + 1

                            temp.append(logout_string)
                    with open('userlog.txt', 'w') as userf:
                        userf.writelines(temp)
        #Loop for ATU command
        elif(user_command == 'ATU'):
            with open('userlog.txt', "r+") as userf:
                active_string = "Active users:\n"
                lines = userf.readlines()
                if len(lines) == 1 :
                    active_string = "No other active users"
                    active_string = active_string.encode('utf-8')
                    connection.sendall(active_string)
                else:
                    for line in lines:
                        line_split = line.split(';')
                        stored_user = line_split[2]
                        stored_user = stored_user.strip()

                        if stored_user != username:

                            active_string = active_string + line

                    active_string = active_string.strip()
                    active_string = active_string.encode('utf-8')
                    connection.sendall(active_string)
        else:
            unknown_string = 'Unknown command'
            unknown_string = unknown_string.strip()
            unknown_string = unknown_string.encode('utf-8')
            connection.sendall(unknown_string)





# sys.exit()



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
    print("Connection from:", client_addr)
    start_new_thread(threaded_client, (client_socket, ))
