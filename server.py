import threading
import server_client_base as scb
import socket


class User():
    def __init__(self, ip, name=None):
        self.__ip = ip
        # My initial thought was to generate unique user name using a counter
        # However, that is not thread safe I think.
        # Just use ip as the unique name.
        # You will be using this with your friends anyway.
        if name is None:
            self.name = ip
        else:
            self.name = name


class Server(scb.ServerClientBase):
    def __init__(self, port):
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: host_name = socket.gethostname()
        host_name = ''
        while True:
            try:
                self.s.bind((host_name, port))
                self.__host_name = host_name 
                self.__port = port
                break
            except:
                port += 1

        self.__connections = {}
        self.__user_name = "Host" # Default host name
        
        th = threading.Thread(target=self.new_conn_handler)
        th.start()

    @property
    def host_name(self):
        return self.__host_name

    @property
    def port(self):
        return self.__port
    
    def send_msg(self, msg):
        if not msg:
            return
        
        msg = self.__user_name + ': ' + msg
        msg = msg.encode()
        self.msg_queue.put(msg) # Display what I am sending on my gui
        
        # It is okay if recv_handler thread comes in at this point and
        #   sends what it received first, resulting in discrepancy
        #   between my gui and the client's gui
        for sock in self.__connections.keys():
            try:
                sock.sendall(msg)
            except:
                sock.close()
                del self.__connections[sock]

    def destroy(self):
        for sock in self.__connections.keys():
            sock.close()
        self.s.close()
   
    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            if not msg:
                break
            
            # TODO: send to all __connections. caution for threading 
            msg_user_name = self.__connections[sock].name + ': ' #not thread safe
            msg = msg_user_name.encode() + msg
            
            sock.sendall(msg)
            self.msg_queue.put(msg)
    
    def new_conn_handler(self):
        while True:
            try:
                self.s.listen(1)	# maximum # of queued __connections
                sock, addr = self.s.accept() 

                user = User(addr[0])

                self.__connections[sock] = user
                print("Connected by", addr)
                
                th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
                th.start()
            except:
                break

        
