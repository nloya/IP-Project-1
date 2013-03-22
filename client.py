import pickle
import socket
from collections import deque
import threading
import random

str = "1. Add RFCs\n2. Request for RFC"

class myThread (threading.Thread):
	def __init__(self, s, opt):
		#self.host = host
		#self.port = port
		self.s = s
		self.opt = opt
		threading.Thread.__init__(self)
	
	def run(self):
		if(opt=="server") # connect to server
			while(True):
				print self.s.recv(1024)
				print str
		elif(opt=="upload"):
			while(True):
				client,addr = self.s.accept()
				

class RFC():
	def __init__(self, rfcno, rfcdesc):
		self.rfcno = rfcno
		self.rfcdesc = rfcdesc

def main():
	rfc = list()
	s = socket.socket()
	print s
	host = socket.gethostbyname(socket.gethostname()) #socket.gethostname() #6.14' #socket.gethostname()
	port = 7734
	
	uploadServer = socket.socket()
	uploadServerHost = socket.gethostbyname(socket.gethostname())
	uploadServerPort = random.randint(49152,65535)
	uploadServer.bind((uploadServerHost,uploadServerPort))
	uploadServer.listen(5)
	thread = myThread(uploadServer, "upload")
	
	#Creating thread for 
	s.connect((host, port))
	thread = myThread(s, "server")
	thread.start()
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