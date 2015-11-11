from tkinter import messagebox
from tkinter import scrolledtext

import tkinter as tk
import client
import server
import sys


DEFAULT_PORT = 10000


class P2pChat(tk.Frame):
    def __init__(self, master=None):
        global DEFAULT_PORT

        master.protocol("WM_DELETE_WINDOW", self.close_app)
        
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=1)
        self.createWidgets()
        
        if messagebox.askyesno("", "Are you hosting the chat room?"):
            self.chat = server.Server(DEFAULT_PORT)
            
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, self.chat.host_ip)
            self.ip_entry.config(state='readonly')
            
            self.port_entry.delete(0, tk.END)
            self.port_entry.insert(0, self.chat.host_port)
            self.port_entry.config(state='readonly')

            self.host_instr_label.pack(side=tk.LEFT)
            # TODO: remove when connected. self.host_instr_label.pack_forget()
        else:
            self.chat = None
            self.ip_entry.insert(0, '0.0.0.0') 
            self.connect_btn.pack(side=tk.LEFT)


        master.bind('<Return>', self.send_msg)
        master.bind('<KP_Enter>', self.send_msg)
        self.display_new_msg()

    def connect_to_host(self):
        host_ip = self.ip_entry.get()
        if not self.validate_ip(host_ip):
            self.show_sys_msg("ip format is invalid")
            return

        port_entry_val = self.port_entry.get()
        if not self.validate_port(port_entry_val):
            msg = "port must be an integer where 1024 < port <= 65535"
            self.show_sys_msg(msg)
            return
  
        try:
            self.chat = client.Client(host_ip, int(port_entry_val))
            self.connect_btn.pack_forget()
            self.ip_entry.config(state='readonly')
            self.port_entry.config(state='readonly')
        except Exception as e:
            self.show_sys_msg(repr(e))
   
    def validate_ip(self, ip):
        parts = ip.split('.')
        if len(parts) != 4:
            return False

        for part in parts:
            try:
                part = int(part)
                if part < 0 or part > 255:
                    return False
            except:
                return False
        return True

    def validate_port(self, port):
        try:
            port = int(port)
            if port > 1024 and port <= 65535:
                return True
            return False
        except:
            return False

    def createWidgets(self):
        global DEFAULT_PORT

        # IP and Port Frame
        ip_port_frame = tk.Frame(self, relief=tk.RAISED, bd=1)
        ip_port_frame.pack(side=tk.TOP, fill=tk.X)

        # IP Frame
        ip_frame = tk.Frame(ip_port_frame)
        ip_frame.pack(side=tk.LEFT)
        
        ip_label = tk.Label(ip_frame, text="ip:")
        ip_label.pack(side=tk.LEFT)
       
        vcmd = (self.register(self.validate_entry_len), '%P', '%W')
       
        ip_max_len = 15
        ip_entry = tk.Entry(ip_frame, width=ip_max_len, \
                            validate='key', vcmd=vcmd)
        ip_entry.pack(side=tk.LEFT)
        ip_entry.insert(0, '') 
        self.ip_entry = ip_entry

        # Port Frame
        port_frame = tk.Frame(ip_port_frame)
        port_frame.pack(side=tk.LEFT)

        port_label = tk.Label(port_frame, text="port:")
        port_label.pack(side=tk.LEFT)

        port_max_len = 5
        port_entry = tk.Entry(port_frame, width=port_max_len, \
                              validate='key', vcmd=vcmd)
        port_entry.pack(side=tk.LEFT)
        port_entry.insert(0, DEFAULT_PORT)
        self.port_entry = port_entry

        # Host Instruction Label
        self.host_instr_label = tk.Label(ip_port_frame, \
            text="<-- Tell your friend this ip and port")
       
        # msg dialogue and entry frame 
        msg_frame = tk.Frame(self)
        msg_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.msg_window = scrolledtext.ScrolledText(msg_frame, height=10, width=80)
        self.msg_window.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.msg_window.config(state=tk.DISABLED)
        
        # msg entry frame
        msg_entry_frame = tk.Frame(msg_frame, relief=tk.RAISED, bd=1)
        msg_entry_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=1)

        self.msg_entry = tk.Entry(msg_entry_frame)
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        send_button = tk.Button(msg_entry_frame)
        send_button["text"] = "Send"
        send_button["command"] = self.send_msg
        send_button.pack(side=tk.RIGHT)

        # client connect to host button
        connect_btn = tk.Button(ip_port_frame)
        connect_btn["text"] = "Connect"
        connect_btn["command"] = self.connect_to_host
        self.connect_btn = connect_btn

    def display_new_msg(self):
        if self.chat is not None:
            msgs = self.chat.get_new_msgs()
            for msg in msgs:
                self.display_msg(msg)
        self.master.after(100, self.display_new_msg)

    def display_msg(self, msg):
        self.msg_window.config(state=tk.NORMAL)
        self.msg_window.insert(tk.END, "%s\n" % msg)
        self.msg_window.yview(tk.END)
        self.msg_window.config(state=tk.DISABLED)

    def send_msg(self, event=None):
        if self.chat is not None:
            msg = self.msg_entry.get()
            self.msg_entry.delete(0, tk.END)
            self.chat.send_msg(msg)

    def validate_entry_len(self, P, W):
        entry = self.master.nametowidget(W)
        if len(P) <= entry['width']:
            return True

        self.bell()
        return False
    
    def show_sys_msg(self, msg):
        if not msg:
            return

        msg = "SYSTEM: " + msg + "."
        self.display_msg(msg)

    def close_app(self):
        if self.chat is not None:
            self.chat.destroy()
        root.destroy()


root = tk.Tk()
p2p_chat = P2pChat(master=root)
p2p_chat.mainloop()

