import threading
import socket


HOST = ''
PORT = 50007


class Server():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
    
    def client_handler(self, conn):
        while True:
            data = conn.recv(1024) # bufsize should be a small power of 2 like 4096
            if not data:
                break

            conn.sendall(data)
        
    def run(self):
        while True:
            self.s.listen(1)	# maximum # of queued connections
            conn, addr = self.s.accept()	# conn is the new socket. addr is the client addr
            print("Connected by", addr) # why can't i use %s?
            
            th = threading.Thread(target=self.client_handler, kwargs={'conn': conn})
            th.start()

        conn.close()


server = Server()
server.run()
