import telnetlib
import tkinter as tk
import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.address_label = tk.Label(self)
        self.address_label["text"] = "FTP Address:"
        self.address_label.pack(side="top")

        self.address_entry = tk.Entry(self)
        self.address_entry.pack(side="top")

        self.port_label = tk.Label(self)
        self.port_label["text"] = "TCP Port:"
        self.port_label.pack(side="top")

        self.port_entry = tk.Entry(self)
        self.port_entry.pack(side="top")

        self.username_label = tk.Label(self)
        self.username_label["text"] = "Username:"
        self.username_label.pack(side="top")

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(side="top")

        self.password_label = tk.Label(self)
        self.password_label["text"] = "Password:"
        self.password_label.pack(side="top")

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(side="top")

        self.connect_button = tk.Button(self)
        self.connect_button["text"] = "Connect"
        self.connect_button["command"] = self.connect_to_receiver
        self.connect_button.pack(side="top")

        self.file_listbox = tk.Listbox(self)
        self.file_listbox.pack(side="bottom")

    def connect_to_receiver(self):
        address = self.address_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            tn = telnetlib.Telnet(address, port)
            tn.read_until(b"login: ")
            tn.write(username.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
            tn.read_until(b"Connected to")
            tn.write(b"vftp\n")
            tn.read_until(b"vftp>")
            tn.write(b"ls\n")

            # Wait for the device to connect
            connected = False
            while not connected:
                time.sleep(1)
                file_list = tn.read_very_eager().decode("utf-8")
                if "Android Debug Bridge" in file_list:
                    connected = True

            file_list = tn.read_until(b"vftp>").decode("utf-8")
            file_list = file_list.split("\n")
            self.file_listbox.delete(0, tk.END)
            for file in file_list:
                if file.startswith("-"):
                    self.file_listbox.insert(tk.END, file)
        except Exception as e:
            print(e)

root = tk.Tk()
app = Application(master=root)
app.mainloop()

