import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import requests, sys

# ------------------ AUTO-UPDATE ------------------
LOCAL_VERSION = "1.2"
UPDATE_URL = "https://raw.githubusercontent.com/sayul-tec/ChatApp/main/version.txt"
CLIENT_URL = "https://raw.githubusercontent.com/sayul-tec/ChatApp/main/client.py"

try:
    latest = requests.get(UPDATE_URL).text.strip()
    if latest != LOCAL_VERSION:
        if messagebox.askyesno("Update Available", f"Version {latest} is available. Update now?"):
            r = requests.get(CLIENT_URL)
            with open(sys.argv[0], "wb") as f:
                f.write(r.content)
            messagebox.showinfo("Update Complete", "Update downloaded! Please restart the app.")
            sys.exit()
except:
    pass
# ----------------------------------------------

# ------------------ CONNECT TO SERVER ------------------
SERVER_IP = "127.0.0.1"  # Localhost for same PC testing
SERVER_PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER_IP, SERVER_PORT))
except Exception as e:
    messagebox.showerror("Connection Error", f"Could not connect to server:\n{e}")
    sys.exit()

# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("Public Chat App")

chat_area = tk.Text(root)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')

msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.X, padx=10, pady=5)

def receive():
    """Receive messages from the server"""
    while True:
        try:
            msg = client.recv(1024).decode()
            chat_area.config(state='normal')
            chat_area.insert(tk.END, msg + "\n")
            chat_area.config(state='disabled')
            chat_area.see(tk.END)
        except:
            break

def send(event=None):
    """Send message to the server"""
    msg = msg_entry.get()
    msg_entry.delete(0, tk.END)
    if msg:
        client.send(f"{username}: {msg}".encode())

msg_entry.bind('<Return>', send)
send_button = tk.Button(root, text="Send", command=send)
send_button.pack(pady=5)

# ------------------ USERNAME ------------------
root.withdraw()
username = simpledialog.askstring("Username", "Enter your username:", parent=root)
if not username:
    messagebox.showerror("Error", "Username cannot be empty!")
    sys.exit()
client.send(username.encode())
root.deiconify()

# ------------------ START RECEIVE THREAD ------------------
threading.Thread(target=receive, daemon=True).start()
root.mainloop()
