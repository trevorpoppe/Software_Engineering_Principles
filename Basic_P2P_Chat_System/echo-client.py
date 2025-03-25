import socket

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to connect to

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # Connect to the server
    message = b"Hello, Server!"
    s.sendall(message)  # Send data to the server
    data = s.recv(1024)  # Receive response from the server

print(f"Received from server: {data.decode()}")

# This code was generated with the help of ChatGPT
