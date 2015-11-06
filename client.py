import threading
import socket
import queue


class Client():
    def __init__(self, host_ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host_ip, port))

        self.msg_queue = queue.Queue()

        th = threading.Thread(target=self.server_handler)
        th.start()

    def get_new_msgs(self):
        msgs = []
        while not self.msg_queue.empty():
            try:
                msg = self.msg_queue.get(block=False)
                msgs.append(msg)
            except queue.Empty():
                return msgs
        return msgs

    def send_msg(self, msg):
        self.s.sendall((msg).encode())
        
    def destroy(self):
        self.s.close()

    def server_handler(self):
        while True:
            msg = self.s.recv(1024)
            if not msg:
                break;
            self.msg_queue.put(msg)
