import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
sock.bind(server_address)
sock.listen(1)
while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            if data:
                connection.sendall(data)
            else:
                break       
    finally:
        # Clean up the connection
        connection.close()