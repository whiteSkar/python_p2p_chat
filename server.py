import threading
import socket

def client_handler(conn):
    while True:
        data = conn.recv(1024) # bufsize should be a small power of 2 like 4096
        if not data:
            break

        conn.sendall(data)
    

HOST = ''
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

while True:
    s.listen(1)	# maximum # of queued connections
    conn, addr = s.accept()	# conn is the new socket. addr is the client addr
    print("Connected by", addr) # why can't i use %s?
    
    th = threading.Thread(target=client_handler, kwargs={'conn': conn})
    th.start()


conn.close()
