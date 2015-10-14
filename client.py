import tkinter as tk
import socket


HOST = '127.0.0.1'	# local host?
PORT = 50007	# same as server


class Client(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
         
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def createWidgets(self):
        self.send_button = tk.Button(self)
        self.send_button["text"] = "Send"
        self.send_button["command"] = self.send_msg
        self.send_button.pack(side="top")

        self.quit_button = tk.Button(self, text="QUIT", fg="red", command=self.close_app)
        self.quit_button.pack(side="bottom")

    def send_msg(self):
        self.s.sendall(('message from client').encode())
        
    def close_app(self):
        self.s.close()
        root.destroy()


root = tk.Tk()
client = Client(master=root)
client.mainloop()




