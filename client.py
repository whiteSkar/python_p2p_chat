import tkinter as tk
from tkinter import messagebox
import socket


HOST = '127.0.0.1'	# local host?
PORT = 50007	# same as server


class Client(tk.Frame):
    def __init__(self, master=None):
        master.protocol("WM_DELETE_WINDOW", self.close_app)
        
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
         
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def createWidgets(self):
        self.msg_window = tk.Text(self, height=10, width=80)
        self.msg_window.pack(side="top")
        
        self.msg_entry = tk.Entry(self)
        self.msg_entry.pack(side="left")

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.send_msg
        self.send_button.pack(side="top")

    def send_msg(self):
        msg = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)
        self.s.sendall((msg).encode())
        
    def close_app(self):
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.s.close()
            root.destroy()


root = tk.Tk()
client = Client(master=root)

client.mainloop()




