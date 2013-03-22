import pickle
import socket

s = socket.socket()
print s
host = socket.gethostbyname(socket.gethostname()) #socket.gethostname() #6.14' #socket.gethostname()
port = 7734
#print host
s.connect((host, port))

#msg = pickle.loads(s.recv(1024))
count = 0
while(True):
	print s.recv(1024)
	'''
	if(count%100000==0):
		print s.recv(1024)
	count+=1
	'''
'''
s1 = socket.socket()
s1.bind((socket.gethostbyname(msg[0]) , msg[1]))
s1.listen(5)

while True:
	client,addr = s1.accept()
	client.send("Msg from Client")
	client.close()
#s.close()
'''