import threading
import server_client_base as scb 
import socket


class Client(scb.ServerClientBase):
    def __init__(self, host_ip, port):
        super().__init__()

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((host_ip, port))

        th = threading.Thread(target=self.recv_handler, kwargs={'sock':self._s})
        th.start()

    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            msg = msg.decode()
            if not msg:
                break

            self._msg_queue.put(msg)

    def send_msg(self, msg):
        if not msg:
            return

        try:
            self._s.sendall(msg.encode())
        except Exception as e:
            self._msg_queue.put("ERROR:", repr(e))
        
    def destroy(self):
        self._s.close()
