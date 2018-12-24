# Importing libraries
import socket
import sys
import os

# Creating an INET and STREAMing socket.
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Receiving user input from the command prompt.
user_input = sys.argv[:]

# Parsing the user input
for i in range(0, len(user_input)):
    if user_input[i-1] == "get" or user_input[i-1] == "put" or user_input[i-1] == "list":
        user_input = user_input [i-3:]

# Server address is a tuple of the host name and the port number. The client enters the port number at execution.
srv_addr = ("localhost", int(user_input[1]))

# Converting the server address to str so it can be printed later.
srv_addr_str = str(srv_addr)

# Encapsulating the attempt of a connect in order to catch any errors in the try-except block.
# Printing appropriate error messages if connection fails.
try:
    print('Connecting to ' + srv_addr_str)
    cli_sock.connect(srv_addr)
    print('Connected to file server on: ', srv_addr_str)

except Exception as e:
    print('Connection could not be made')
    print(e)
    # Exit to indicate that an error has occured.
    exit(1)

# Check if there is a filename. Otherwise, the program will continue, in the case of a list command is given.
try:
    filename = user_input[3]
    # print(filename)
except Exception as e:
    print(' ')

try:
    try:
        while True:

            ''' UPLOADING/PUT
            Client requests put operation - sends client request for server to execute appropriate case.
            Opens given filename, reads and sends each file to the server.
            Catches errors with try-except and gives status report. '''
            if user_input[2] == 'put':
                user_input = " ".join(user_input)
                cli_sock.sendall(str.encode(user_input))
                try:
                    # Checking the file is not empty or too large
                    print(os.path.getsize(__file__))
                    if os.path.getsize(__file__) <= 0 | os.path.getsize(__file__) >= 1073741824:
                        print('File size is not appropriate. Size: ', os.path.getsize(__file__))
                        break
                    f = open(filename, 'rb')
                    line = f.read(4094)
                    while line:
                        cli_sock.send(line)
                        # print('Sent ', repr(line))
                        line = f.read(4096)
                    f.close()
                    print('Sent file successfully.')
                    break
                except Exception as e:
                    print('Could not send file to server.')

            ''' DOWNLOADING/GET
            Client requests get operation - sends client request for server to execute appropriate case.
            Opens given filename, receives each line and writes it the the file from server.
            Catches errors with try-except and gives status report. '''
            if user_input[2] == 'get':
                user_input = " ".join(user_input)
                cli_sock.sendall(str.encode(user_input))
                try:
                    f = open(filename, 'xb')
                    data = cli_sock.recv(4096)
                    while data:
                        f.write(data)
                        data = cli_sock.recv(4096)
                    f.close()
                    print('Received file successfully.')
                    break
                except FileExistsError:
                    print("The file already exists")

            ''' LIST 
            Client requests list operation - sends client request for server to execute appropriate case.
            Receives the directories data and prints.
            Catches errors with try-except and gives status report. '''
            if user_input[2] == 'list':
                user_input = " ".join(user_input)
                cli_sock.sendall(str.encode(user_input))
                try:
                    data = cli_sock.recv(4096)
                    directories = data.decode().strip().split()
                    print('Directory: ', directories)
                    print('Obtained directory successfully.')
                    break
                except Exception as e:
                    print('Could not receive server directories.')
    except Exception as e:
        print('Could not process request.')

# Closing connection
finally:
    cli_sock.close()
    print('Closing connecting from server address: ', srv_addr_str)
