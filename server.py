import socket
import pickle
import threading



class myThread (threading.Thread):
	def __init__(self, client, addr):
		self.client = client
		self.addr = addr
		threading.Thread.__init__(self)
	
	def run(self):
		self.client.send("Thank you for connecting")
		conn=0
		while(True):
			conn+=1
			if(conn==142312345):
				self.client.send("THANK YOU")


def main():
	s = socket.socket()
	print s
	host = socket.gethostbyname(socket.gethostname())
	port = 7734
	#print host
	s.bind((host, port))
	prev = []
	s.listen(5)
	conn = 0
	while True:
		conn+=1
		client, addr = s.accept()		
		thread = myThread(client, addr)
		thread.start()
		
		
		
		
		
		
		
'''
def listen(client, addr):
	client.send("Thank you for connecting")
	#client.close()
	
	if conn%2==0:
		print 'Connection from', addr
		client.send(pickle.dumps(prev))
	#print client.recv(1024)
	#print s.accept()
	else:
		print addr[0], addr[1]
		prev.append(addr[0])
		prev.append(addr[1])
		print client
		print 'Connection from', addr
		client.send(pickle.dumps(addr))
	#client.close()
	'''
	
	
main()