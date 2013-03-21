import socket
import pickle

s = socket.socket()

host = socket.gethostbyname('10.139.67.49') #socket.gethostname() #6.14' #socket.gethostname()
port = 7734
#print host
s.connect((host, port))
#while True:
	#s.send
#while True:
msg = pickle.loads(s.recv(1024))
print msg[0],msg[1]
s.close()

s = socket.socket()
s.connect((socket.gethostbyname(msg[0]),msg[1]))
print s.recv(1024)
#s.close()