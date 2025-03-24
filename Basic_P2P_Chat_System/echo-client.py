import socket

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()  # Accept a connection
    with conn:
        print(f"Connected by {addr}")
        data = conn.recv(1024)
        conn.sendall(data)  # Echo back the received data

# This code was generated with the help of ChatGPT
