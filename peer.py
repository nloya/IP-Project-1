import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname(socket.gethostname())
port = 53388

s.connect((host,port))
print("Peer: %s" %s.recv(1024))
s.close()