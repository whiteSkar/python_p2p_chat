import threading
import server_client_base as scb 
import socket


class Client(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host_ip, port))

        th = threading.Thread(target=self.recv_handler, kwargs={'sock':self.s})
        th.start()

    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            if not msg:
                break
            self.msg_queue.put(msg)

    def send_msg(self, msg):
        if not msg:
            return
        try:
            self.msg_queue.put("send_msg is called".encode())
            self.s.sendall(msg.encode())
            self.msg_queue.put("send_msg is done!!".encode())
        except:
            self.msg_queue.put("Error while send_msg".encode())
            # TODO throw custom exception and let caller catch and display error
            pass
        
    def destroy(self):
        self.s.close()
