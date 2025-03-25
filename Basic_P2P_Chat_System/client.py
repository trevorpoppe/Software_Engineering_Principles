import socket

HOST = "127.0.0.1"
PORT = 65432

def send_message(sender, receiver, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        command = f"SEND|{sender}|{receiver}|{message}"
        s.sendall(command.encode())
        response = s.recv(1024).decode()
        print("Server:", response)

def receive_messages(receiver):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        command = f"RECEIVE|{receiver}"
        s.sendall(command.encode())
        response = s.recv(1024).decode()
        print("Messages for", receiver, ":\n", response)

# Example usage
if __name__ == "__main__":
    while True:
        action = input("Enter 'send' to send a message or 'receive' to check messages: ").strip().lower()
        if action == "send":
            sender = input("Your name: ")
            receiver = input("Recipient name: ")
            message = input("Message: ")
            send_message(sender, receiver, message)
        elif action == "receive":
            receiver = input("Your name: ")
            receive_messages(receiver)
        else:
            print("Invalid input")
