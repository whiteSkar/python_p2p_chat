import threading
import server_client_base as scb
import socket


class Server(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__(host_ip, port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: host_name = socket.gethostname()
        self.__host_name = ''
        self.__port = port
        self.s.bind((self.__host_name, self.__port))
        # TODO: automatic change of port if port is being used
        self.connections = {}
        
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
        msg = msg.encode()
        self.msg_queue.put(msg) # Display what I am sending on my gui
        
        # It is okay if recv_handler thread comes in at this point and
        #   sends what it received first, resulting in discrepancy
        #   between my gui and the client's gui
        for sock in self.connections:
            try:
                sock.sendall(msg)
            except:
                sock.close()
                del self.connections[sock]

    def destroy(self):
        for conn in self.connections.keys():
            conn.close()
        self.s.close()
   
    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            if not msg:
                break
            
            # TODO: send to all connections. caution for threading 
            sock.sendall(msg)
            self.msg_queue.put(msg)
    
    def new_conn_handler(self):
        while True:
            try:
                self.s.listen(1)	# maximum # of queued connections
                sock, addr = self.s.accept() 
                self.connections[sock] = addr
                print("Connected by", addr) # why can't i use %s?
                
                th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
                th.start()
            except:
                break

        
