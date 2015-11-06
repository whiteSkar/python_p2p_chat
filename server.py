import threading
import server_client_base as scb
import socket


class Server(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__(host_ip, port)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #host_name = socket.gethostname()
        self.s.bind(('', port))
        print("Server binded on port:", port)

        self.connections = {}
    
    def send_msg(self, msg):
        for conn in self.connections:
            try:
                conn.sendall(msg.encode())
            except:
                conn.close()
                self.connections.remove(conn)
        
    def destroy(self):
        for conn in self.connections.keys():
            conn.close()
        self.s.close()
   
    def run(self):
        th = threading.Thread(target=self.incoming_handler)
        th.start()
        
    def client_handler(self, conn):
        while True:
            data = conn.recv(1024) # bufsize should be a small power of 2 like 4096
            if not data:
                break
            
            # send to all connections. caution for threading 
            conn.sendall(data)
    
    def incoming_handler(self):
        while True:
            self.s.listen(1)	# maximum # of queued connections
            conn, addr = self.s.accept()	# conn is the new socket. addr is the client addr
            self.connections[conn] = addr
            print("Connected by", addr) # why can't i use %s?
            
            th = threading.Thread(target=self.client_handler, kwargs={'conn': conn})
            th.start()

        
