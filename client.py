import threading
import server_client_base as scb 
import socket


class Client(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__(host_ip, port)
        print("start")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host_ip, port))
        print("done")

        th = threading.Thread(target=self.server_handler)
        th.start()

    def send_msg(self, msg):
        self.s.sendall(msg.encode())
        
    def destroy(self):
        self.s.close()

    def server_handler(self):
        while True:
            msg = self.s.recv(1024)
            if not msg:
                break;
            self.msg_queue.put(msg)
