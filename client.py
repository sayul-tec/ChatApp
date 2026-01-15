import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import time
import sys
import requests

# ------------------ AUTO-UPDATE ------------------
LOCAL_VERSION = "1.4"
UPDATE_URL = "https://raw.githubusercontent.com/sayul-tec/ChatApp/main/version.txt"
CLIENT_URL = "https://raw.githubusercontent.com/sayul-tec/ChatApp/main/ssss.py"

def check_update():
    try:
        latest = requests.get(UPDATE_URL, timeout=3).text.strip()
        if latest != LOCAL_VERSION:
            if messagebox.askyesno("Update Available", f"Version {latest} is available. Update now?"):
                data = requests.get(CLIENT_URL).content
                with open(sys.argv[0], "wb") as f:
                    f.write(data)
                messagebox.showinfo("Update Complete",
                                    "Update downloaded! Please restart the app to apply changes.")
                sys.exit()
    except:
        print("Auto-update failed or offline.")


# ------------------ SPLASH ------------------
def show_splash():
    win = tk.Toplevel()
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    win.geometry(f"600x400+{screen_w//2-300}+{screen_h//2-200}")
    canvas = tk.Canvas(win, bg="#101018", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Robot logo
    robot = canvas.create_text(300, 140, text="🤖", font=("Arial", 100), fill="#000000")
    powered = canvas.create_text(300, 260, text="Powered by ChatBotX Core",
                                 font=("Arial", 22), fill="#000000")

    # Fade-in
    for i in range(0, 101, 3):
        color = f"#{i:02x}{i:02x}{i:02x}"
        canvas.itemconfig(robot, fill=color)
        canvas.itemconfig(powered, fill=color)
        win.update()
        time.sleep(0.02)

    time.sleep(0.5)

    # Fade-out
    for i in range(100, -1, -4):
        color = f"#{i:02x}{i:02x}{i:02x}"
        canvas.itemconfig(robot, fill=color)
        canvas.itemconfig(powered, fill=color)
        win.update()
        time.sleep(0.015)

    win.destroy()
    time.sleep(0.1)


# ------------------ CHAT CLIENT ------------------
class ChatClient(tk.Tk):
    def __init__(self, username, server_ip="127.0.0.1", server_port=5555):
        super().__init__()
        self.title("ChatBotX")
        self.geometry("900x600")
        self.configure(bg="#0f0f17")

        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Cannot connect: {e}")
            sys.exit()

        self.client_socket.send(self.username.encode())

        # Layout
        self.sidebar = tk.Frame(self, bg="#14141c", width=220)
        self.sidebar.pack(side="left", fill="y")

        self.chat_frame = tk.Frame(self, bg="#0f0f17")
        self.chat_frame.pack(side="right", fill="both", expand=True)

        self.chat_text = scrolledtext.ScrolledText(self.chat_frame, state="disabled",
                                                   bg="#0f0f17", fg="white", font=("Segoe UI", 14))
        self.chat_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry_frame = tk.Frame(self.chat_frame, bg="#0f0f17")
        self.entry_frame.pack(fill="x", padx=10, pady=5)

        self.entry = tk.Entry(self.entry_frame, font=("Segoe UI", 14))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side="right")

        # Sidebar channels
        tk.Label(self.sidebar, text="💬 Channels", font=("Segoe UI", 18, "bold"), bg="#14141c", fg="white").pack(pady=10)
        for ch in ["general", "chat", "gaming", "bots", "admin"]:
            b = tk.Button(self.sidebar, text=f"# {ch}", font=("Segoe UI", 14),
                          bg="#14141c", fg="white", activebackground="#1f1f2b", relief="flat")
            b.pack(fill="x", padx=10, pady=2)

        # Start receiving messages
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def receive_loop(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode()
                if msg:
                    self.chat_text.configure(state="normal")
                    self.chat_text.insert(tk.END, msg + "\n")
                    self.chat_text.configure(state="disabled")
                    self.chat_text.see(tk.END)
            except:
                break

    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if msg:
            self.client_socket.send(f"{self.username}: {msg}".encode())
            self.entry.delete(0, tk.END)


# ------------------ START ------------------
if __name__ == "__main__":
    check_update()

    # Username dialog
    root = tk.Tk()
    root.withdraw()
    username = simpledialog.askstring("Username", "Enter your username:")
    if not username:
        sys.exit()
    root.destroy()

    show_splash()
    app = ChatClient(username)
    app.mainloop()
