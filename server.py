import threading
import server_client_base as scb
import socket
import sys


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
       
        self.lock = threading.Lock()
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
        
        with self.lock:
            self.send_msg_to_all(msg)

    def send_sys_msg_to_one_user(self, sock, msg):
        if not msg:
            return

        msg = 'SYSTEM: ' + msg
        msg = msg.encode()

        sock.sendall(msg) 

    def send_sys_msg_to_all(self, msg):
        if not msg:
            return

        msg = 'SYSTEM: ' + msg
        msg = msg.encode()
        
        self.send_msg_to_all(msg)

    # Pre: Call with lock for thread safety
    def send_msg_to_all(self, msg):
        disconnected = []
        for sock in self.__connections.keys():
            try:
                sock.sendall(msg)
            except Exception as e:
                print("error:", repr(e))
                raise
                # Not sure if there will be any case
                disconnected.append(sock)
        for sock in disconnected:
            self.handle_disconnected(sock)

        # To ensure what I see is what they see
        self.msg_queue.put(msg)


    def destroy(self):
        with self.lock:
            for sock in self.__connections.keys():
                sock.close()
            self.s.close()
   
    def recv_handler(self, sock):
        while True:
            msg = sock.recv(1024)
            msg = msg.decode()
            msg_type = self.determine_msg_type(msg)

            if msg_type == 1:
                with self.lock:
                    self.handle_disconnected(sock)
            elif msg_type == 2:
                with self.lock:
                    self.change_user_name(sock, msg[4:])
            else:
                with self.lock:
                    msg_user_name = self.__connections[sock].name + ': '
                    msg = msg_user_name + msg
                    
                    self.send_msg_to_all(msg.encode())

    # Pre: Call with lock for thread safety
    def change_user_name(self, user_sock, new_user_name):
        # TODO: validate user name

        for sock, user in self.__connections.items():
            if user.name == new_user_name and sock is not user_sock:
                self.send_sys_msg_to_one_user(user_sock, 'Name taken')
                return
        
        if self.__connections[user_sock].name == new_user_name:
            self.send_sys_msg_to_one_user(user_sock, 'Already your name')
            return

        sys_msg = 'User ' + self.__connections[user_sock].name
        self.__connections[user_sock].name = new_user_name
        sys_msg += ' changed user name to ' + new_user_name
        self.send_sys_msg_to_all(sys_msg)

    def determine_msg_type(self, msg):
        if not msg:
            return 1

        if len(msg) >= 5 and msg[:4] == "/nc ":
            return 2

        return 3

    def new_conn_handler(self):
        while True:
            try:
                self.s.listen(5)
                sock, addr = self.s.accept() 

                user = User(addr[0])
                
                with self.lock:
                    self.__connections[sock] = user
                self.show_msg(user.name + " has joined the room")
                print("Connected by", addr)
                
                th = threading.Thread(target=self.recv_handler, kwargs={'sock': sock})
                th.start()
            except:
                break
    
    # Pre: call with lock for thread safety
    def handle_disconnected(self, sock):
        dis_msg = self.__connections[sock].name + " is disconnected" 
        self.msg_queue.put(dis_msg.encode())
        sock.close()
        del self.__connections[sock]


    def show_msg(self, msg):
        self.msg_queue.put(msg.encode())
        
