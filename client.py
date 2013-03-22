import pickle
import socket
from collections import deque
import threading
import random

str = "1. Add RFCs\n2. Request for RFC"

class myThread (threading.Thread):
	def __init__(self, opt, sock=None, client=None, addr=None):
		#self.host = host
		#self.port = port
		
		threading.Thread.__init__(self)
		self.opt = opt
		if(client is None and addr is None):
			#print("In if %s --- %s" %(self.opt,self))
			self.sock = sock				
		elif(sock is None):
			#print("In elif %s --- %s" %(self.opt,self))
			self.client = client
			self.addr = addr
		else:
			print("Not enough or appropriate arguments")
		#threading.Thread.__init__(self)
	
	def run(self):
		if(cmp(self.opt,"server")==0): #connect to server
			#print("In If %s --- %s" %(self.opt,self))
			while(True):
				print self.sock.recv(1024)
				print str
		elif(cmp(self.opt,"upload")==0):
			#print("In Elif %s --- %s" %(self.opt,self))
			while(True):				
				client,addr = self.sock.accept()				
				thread = myThread("peer", client=client,addr=addr)
				thread.start()
		else: # self.opt == peer
			self.client.send("Thanks man from Peer")
			self.client.close()

class RFC():
	def __init__(self, rfcno, rfcdesc):
		self.rfcno = rfcno
		self.rfcdesc = rfcdesc

def main():
	rfc = list()
	
	uploadServer = socket.socket()
	uploadServerHost = socket.gethostbyname(socket.gethostname())
	uploadServerPort = random.randint(49152,65535)
	uploadServer.bind((uploadServerHost,uploadServerPort))
	uploadServer.listen(5)
	print("Listening on Host: %s & Port: %s" %(uploadServerHost,uploadServerPort))
	thread1 = myThread("upload", sock=uploadServer)
	thread1.start()
	
	#Creating thread for 
	print("Server starts...")
	s = socket.socket()
	print s
	host = socket.gethostbyname(socket.gethostname()) #socket.gethostname() #6.14' #socket.gethostname()
	port = 7734
	s.connect((host, port))
	thread2 = myThread("server", sock=s)
	thread2.start()
	#msg = pickle.loads(s.recv(1024))
	count = 0
	while(True):		
		#print "1. Add RFCs\n2. Request for RFC"
		option = input()
		if(option==1):		
			rfcno = raw_input("Enter RFC#: ")
			rfcdesc = raw_input("Enter Title for RFC: ")		
			rfc.append(RFC(rfcno,rfcdesc))
			print("RFC# %s having Title: \"%s\" added to the list. Total Count of RFCs: %s" %(rfc[len(rfc)-1].rfcno, rfc[len(rfc)-1].rfcdesc, len(rfc)))
			print str
		else:
			print("Incorrect Option Entered")
			print str
			
main()
		
		
		
		
		
		
		
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