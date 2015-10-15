import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import threading
import socket
import queue


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

        self.msg_queue = queue.Queue()

        th = threading.Thread(target=self.server_handler)
        th.start()

        self.display_new_msg()

    def createWidgets(self):
        self.msg_window = scrolledtext.ScrolledText(self, height=10, width=80)
        self.msg_window.pack(side=tk.TOP)
        self.msg_window.config(state=tk.DISABLED)
        
        self.msg_entry = tk.Entry(self,width=70)
        self.msg_entry.pack(side=tk.LEFT)

        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.send_msg
        self.send_button.pack(side=tk.RIGHT)

    def display_new_msg(self):
        while not self.msg_queue.empty():
            try:
                msg = self.msg_queue.get(block=False)
                
                self.msg_window.config(state=tk.NORMAL)
                self.msg_window.insert(tk.END, "%s\n" % msg.decode())
                self.msg_window.yview(tk.END)
                self.msg_window.config(state=tk.DISABLED)
            except queue.Empty():
                pass
        self.master.after(100, self.display_new_msg)

    def send_msg(self):
        msg = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)
        self.s.sendall((msg).encode())
        
    def close_app(self):
        #if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.s.close()
            root.destroy()

    def server_handler(self):
        while True:
            msg = self.s.recv(1024)
            if not msg:
                break;
            self.msg_queue.put(msg)


root = tk.Tk()
client = Client(master=root)
client.mainloop()




