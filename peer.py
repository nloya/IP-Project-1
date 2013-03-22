import socket

s = socket.socket()

host = socket.gethostbyname(socket.gethostname())
port = 58994

s.connect((host,port))
print("Peer: %s" %s.recv(1024))
s.close()