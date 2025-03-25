import socket
import sqlite3
import threading

HOST = "127.0.0.1"
PORT = 65432

# Database setup
def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            delivered BOOLEAN DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Function to save a message
def save_message(sender, receiver, message):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)", 
                   (sender, receiver, message))
    conn.commit()
    conn.close()

# Function to retrieve undelivered messages
def get_messages(receiver):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, sender, message FROM messages WHERE receiver = ? AND delivered = 0", (receiver,))
    messages = cursor.fetchall()

    # Mark messages as delivered
    for msg in messages:
        cursor.execute("UPDATE messages SET delivered = 1 WHERE id = ?", (msg[0],))
    
    conn.commit()
    conn.close()
    return messages

# Handle client connections
def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            
            parts = data.split("|")
            command = parts[0]

            if command == "SEND":
                sender, receiver, message = parts[1], parts[2], parts[3]
                save_message(sender, receiver, message)
                conn.sendall(b"Message stored\n")
            
            elif command == "RECEIVE":
                receiver = parts[1]
                messages = get_messages(receiver)
                response = "\n".join([f"From {msg[1]}: {msg[2]}" for msg in messages]) or "No new messages"
                conn.sendall(response.encode())

# Start the server
def start_server():
    init_db()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server listening...")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    start_server()
