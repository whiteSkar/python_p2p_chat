import tkinter as tk
import client
import server

from tkinter import messagebox
from tkinter import scrolledtext


HOST = '127.0.0.1'	# local host?
PORT = 50007	# same as server


class P2pChat(tk.Frame):
    def __init__(self, master=None):
        master.protocol("WM_DELETE_WINDOW", self.close_app)
        
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
        if messagebox.askyesno("", "Are you hosting the chat room?"):
            self.chat = server.Server(None, PORT)
            self.chat.run()
        else:
            self.chat = client.Client(HOST, PORT)
        
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
        msgs = self.chat.get_new_msgs()
        for msg in msgs:
            self.msg_window.config(state=tk.NORMAL)
            self.msg_window.insert(tk.END, "%s\n" % msg.decode())
            self.msg_window.yview(tk.END)
            self.msg_window.config(state=tk.DISABLED)
        self.master.after(100, self.display_new_msg)

    def send_msg(self):
        msg = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)
        self.chat.send_msg(msg)

    def close_app(self):
        self.chat.destroy()
        root.destroy()


root = tk.Tk()
p2p_chat = P2pChat(master=root)
p2p_chat.mainloop()




