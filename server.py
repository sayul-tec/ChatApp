import socket
import threading

clients = []
usernames = []

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, sender=client)
        except:
            if client in clients:
                index = clients.index(client)
                username = usernames[index]
                clients.remove(client)
                usernames.remove(username)
                broadcast(f"*** {username} left the chat ***".encode())
            client.close()
            break

def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))  # listen on all IPs
    server.listen()
    print("Server running on port 5555...")

    while True:
        client, address = server.accept()
        print(f"Connection from {address}")
        client.send("USERNAME".encode())
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)
        broadcast(f"*** {username} joined the chat ***".encode())
        threading.Thread(target=handle, args=(client,)).start()

receive()
