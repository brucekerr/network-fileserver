# Importing libraries
import socket
import os
import sys

# Creating an INET and STREAMing socket.
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Receiving port number from command line
port_number = sys.argv[1]

# Attempting to establish point of connection with a try-catch.
try:
    srv_sock.bind(("localhost", int(port_number)))
    srv_sock.listen(10)
    print('IP Address of server: ', socket.gethostbyname(socket.gethostname()),
          'Port number: ', int(port_number))
except Exception as e:
    print('Connection could not be made')
    print(e)


while True:
    try:
        # Attempting to connect to client
        print("Waiting for new client...")
        cli_sock, cli_addr = srv_sock.accept()

        # Client address to a string to be printed
        cli_addr_str = str(cli_addr)

        print ('Got connection from', cli_addr_str)

        while True:
            # Receiving client data
            client_data = cli_sock.recv(4096)

            # Preparing the data for use
            data = client_data.decode().strip().split()

            command = data[2]

            # Checking to see if there is a filename for use
            try:
                filename = data[3]
            except Exception as e:
                print('There is no file name')
            else:
                filename = data[3]

            ''' SENDING/GET
            Server receives get operation.
            Opens given filename, reads and sends each line of file to the client.
            Catches errors with try-except and gives status report. '''
            if command == 'get':
                print('Server received get function request')
                try:
                    f = open(filename, 'rb')
                    print("File opened for writing")
                    line = f.read(4094)
                    while line:
                        cli_sock.send(line)
                        line = f.read(4096)
                    f.close()
                    print('Sent file successfully.')
                    break
                except Exception as e:
                    print('Could not send file to client.')
                break

            ''' DOWNLOADING/PUT
            Server receives put operation.
            Opens given filename, receives each line of file from client and writes to a file.
            Catches errors with try-except and gives status report. '''
            if command == 'put':
                print ('Server received put function request')
                try:
                    f = open(filename, 'xb')
                    print('File opened')
                    data = cli_sock.recv(4096)
                    while data:
                        f.write(data)
                        data = cli_sock.recv(4096)
                    f.close()
                    print('Stored file successfully.')
                except Exception as e:
                    print('Could not receive file from client. File already exists.')
                break

            ''' LIST 
            Server receives list operation.
            Uses os library to find files in the local folder of the server.
            Sends this data to the user.
            Catches errors with try-except and gives status report. '''

            if command == 'list':
                try:
                    line = " ".join(os.listdir())
                    cli_sock.sendall(str.encode(line))
                    print('Returned directory successfully.')
                except Exception as e:
                    print('Could not list directories.')
                break
    finally:
        print('Closing connections from client address: ', cli_addr_str)
        print(" ")
        print(" ")
        cli_sock.close()

# Close the server socket as well to release its resources back to the OS

srv_sock.close()