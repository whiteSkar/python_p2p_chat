import socket

HOST = '127.0.0.1'	# local host?
PORT = 50007	# same as server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(b'Hello world')	# try non binary
data = s.recv(1024)
s.close()
print("Received", repr(data))
