import socket
import threading
import tkinter as tk
from tkinter import simpledialog

# ------------------ Connect to server ------------------
SERVER_IP = simpledialog.askstring("Server IP", "Enter server IP:")
SERVER_PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

# ------------------ GUI Setup ------------------
root = tk.Tk()
root.title("Public Chat")

chat_area = tk.Text(root)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')

msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.X, padx=10, pady=5)

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            chat_area.config(state='normal')
            chat_area.insert(tk.END, message + "\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
        except:
            break

def send(event=None):
    message = msg_entry.get()
    msg_entry.delete(0, tk.END)
    if message:
        client.send(f"{username}: {message}".encode())

msg_entry.bind('<Return>', send)
send_button = tk.Button(root, text="Send", command=send)
send_button.pack(pady=5)

# ------------------ Username ------------------
username = simpledialog.askstring("Username", "Enter your username:")
client.send(username.encode())

threading.Thread(target=receive, daemon=True).start()
root.mainloop()
