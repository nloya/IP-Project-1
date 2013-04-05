import pickle
import socket
from collections import deque
import threading
import random
import time
import os
import sys
import platform
import datetime

ipstr = "1. Add RFCs locally\n2. ADD RFCs to Server\n3. Lookup\n4. List"
rfc = list()
rfcsent = 0 # will keep counter of how many RFCs have been sent to the server and will only send those RFCs which have not been sent

class RFC():
	def __init__(self, rfcno, rfcdesc):
		self.rfcno = rfcno
		self.rfcdesc = rfcdesc

class myThread (threading.Thread):
	def __init__(self, opt, sock=None, client=None, addr=None, uphost=None, upport=None, option=None, msg=None):
		#self.host = host
		#self.port = port
		
		threading.Thread.__init__(self)
		self.opt = opt
		self.option = option
		self.sock = sock
		self.uphost = uphost
		self.upport = upport
		self.client = client
		self.addr = addr
		self.msg = msg
		"""
		if(client is None and addr is None): # Either came from upload/server
			#print("In if %s --- %s" %(self.opt,self))
			self.sock = sock
			self.uphost = uphost
			self.upport = upport
			print("Info: %s %s %s" %(self.sock,self.uphost,self.upport))
		elif(sock is None): # upload spawning a peer
			#print("In elif %s --- %s" %(self.opt,self))
			self.client = client
			self.addr = addr
		else:
			print("Not enough or appropriate arguments")
		#threading.Thread.__init__(self)
		"""
	
	def run(self):
		if(cmp(self.opt,"upload")==0):
			#print("In Elif %s --- %s" %(self.opt,self))
			while(True):				
				client,addr = self.sock.accept()
				print('*'*40)
				print(client)
				print(addr)
				print('*'*40) 
				print("Info1: %s %s %s" %(self.sock,self.uphost,self.upport))
				#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				thread = myThread("replytopeer", client=client,addr=addr)
				thread.start()
		else: # cmp(self.opt,"replytopeer")==0
			msg = self.client.recv(1024)
			lines = msg.split('\n')
			words = lines[0].split(' ')
			if(cmp(words[0],"GET")==0):
				t = datetime.datetime.now()				
				try:					
					filename = 'C:\Users\Niks\Downloads\Tmp\%s.txt' %words[2]
					f = open(filename, 'r')
					statbuf = os.stat(filename)	
					msg = "P2P-CI/1.0 200 OK\nDate: %s, %s %s %s %s\nOS: %s %s\nLast Modified: %s\nContent-Length: %s\nContent-Type: text/plain\n" \
					   %(t.strftime("%a"),t.strftime("%d"),t.strftime("%b"),t.strftime("%Y"),t.strftime("%H:%M:%S"),platform.system(),os.name,statbuf.st_mtime,statbuf.st_size)
					msg+=f.read()												
				except IOError as e:
					msg = "P2P-CI/1.0 404 Not Found\nDate: %s, %s %s %s %s\nOS: %s %s\nLast Modified: %s\nContent-Length: %s\nContent-Type: text/plain\n" \
					   %(t.strftime("%a"),t.strftime("%d"),t.strftime("%b"),t.strftime("%Y"),t.strftime("%H:%M:%S"),platform.system(),os.name,statbuf.st_mtime,statbuf.st_size)
					print "I/O error({0}): {1}".format(e.errno, e.strerror)
					msg+="File Not Found"
			self.client.send(msg)
			"""
		elif(cmp(self.opt,"reqfrompeer")==0): # self.opt == peer
			print self.msg
			self.sock.send(self.msg)
			print self.sock.recv(1024)
			#self.sock.close()
			"""

class pseudoThread():
	def __init__(self, opt, sock=None, client=None, addr=None, uphost=None, upport=None, option=None):
		#self.host = host
		#self.port = port
		
		#threading.Thread.__init__(self)
		self.opt = opt
		self.option = option
		self.sock = sock
		self.uphost = uphost
		self.upport = upport
		self.client = client
		self.addr = addr
	
	def start(self):
		if(cmp(self.opt,"server")==0): #connect to server
			#print("In If %s --- %s" %(self.opt,self))
			if(self.option==2):
				global rfcsent
				while(rfcsent != len(rfc)):
					#self.sock.recv(1024)
					self.sock.send("ADD RFC %s P2P-CI/1.0\nHost: %s\nPort: %s\nTitle: %s" %(rfc[rfcsent].rfcno,socket.gethostbyname(socket.gethostname()),self.upport,rfc[rfcsent].rfcdesc))
					print(self.sock.recv(1024)) # blocking call
					rfcsent+=1
					#self.sock.recv(1024)
					#print ipstr
				#print ipstr
				#print "HERE"
				#self.sock.close()
			elif(self.option==3): # Lookup
				temprfcno = getinput("Enter RFC# to query to Server: ")
				temptitle = raw_input("Enter the Title of the RFC: ")
				self.sock.send("LOOKUP RFC %s P2P-CI/1.0\nHost: %s\nPort: %s\nTitle: %s" %(temprfcno,socket.gethostbyname(socket.gethostname()),self.upport,temptitle))
				print('*'*40)
				msg=self.sock.recv(4096).rstrip()				
				print('*'*40)
				lines = msg.split('\n')				
				print('*'*40)
				#print("Select Option")
				for i in range(1,len(lines)):
					print(str(i) + " --> " + lines[i])
				print("0 --> Do Nothing")
				x = input("Select Option: ")				
				getdata(lines[x])
			elif(self.option==4): # List
				self.sock.send("LIST ALL P2P-CI/1.0\nHost: %s\nPort: %s\n" %(socket.gethostbyname(socket.gethostname()),self.upport))
				msg=self.sock.recv(4096).rstrip()				
				print('*'*40)
				lines = msg.split('\n')				
				print('*'*40)
				for i in range(1,len(lines)):
					print(str(i) + " --> " + lines[i])
				print("0 --> Do Nothing")			

def main():
	#rfcsent = 0
	#rfcno = getinput("Enter RFC#: ")
	#rfcdesc = raw_input("Enter Title for RFC: ")		
	#rfc.append(RFC(rfcno,rfcdesc))
	#print("RFC# %s having Title: \"%s\" added to the list. Total Count of RFCs: %s" %(rfc[len(rfc)-1].rfcno, rfc[len(rfc)-1].rfcdesc, len(rfc)))
	uploadServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	uploadServerHost = socket.gethostbyname(socket.gethostname())
	uploadServerPort = random.randint(49152,65535)
	uploadServer.bind((uploadServerHost,uploadServerPort))
	uploadServer.listen(5)
	print("Listening on Host: %s & Port: %s" %(uploadServerHost,uploadServerPort))
	thread = myThread("upload", sock=uploadServer,uphost=uploadServerHost,upport=uploadServerPort)
	thread.start()
	
	#Creating thread for 
	#print("Server starts...")
	
	#print s
	host = socket.gethostbyname(socket.gethostname())
	port = 7734
	
	#msg = pickle.loads(s.recv(1024))
	count = 0
	while(True):
		#time.sleep(3)
		print ipstr
		try:
			option = int(raw_input()) # input() gives integer and raw_input() gives string
			if(option==1):		
				#rfcno = raw_input("Enter RFC#: ")
				#rfcdesc = raw_input("Enter Title for RFC: ")		
				rfcno = getinput("Enter RFC#: ")
				rfcdesc = raw_input("Enter Title for RFC: ")
				rfcPresent = False
				for r in rfc:
					if r.rfcno == rfcno:						
						rfcPresent = True
						break
				if(rfcPresent):
					print("RFC already exists")
				else:
					rfc.append(RFC(rfcno,rfcdesc))
					f = file('C:\Users\Niks\Downloads\Tmp\%s.txt' %rfcno, 'w')
					f.write(str(rfcno) + "  " + rfcdesc)
					f.close()
					print("RFC# %s having Title: \"%s\" added to the list. Total Count of RFCs: %s" %(rfc[len(rfc)-1].rfcno, rfc[len(rfc)-1].rfcdesc, len(rfc)))				
					#print ipstr
			elif(option>=2 and option <= 4):
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((host, port))
				pthread = pseudoThread("server", sock=s, uphost=uploadServerHost, upport=uploadServerPort, option=option)
				pthread.start()						
			else:
				print("Incorrect Option Entered")
				#print ipstr
		except ValueError:
			print("Invalid Characters Entered")

def getinput(msg):
	try:
		return int(raw_input(msg))
	except ValueError:
		print("Invalid Characters enterd")
		return getinput(msg)

def getdata(line):
	print("Line: " + line)
	words = line.split(" ")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tport = int(words[3])
	msg = "GET RFC %s P2P-CI/1.0\nHost: %s\nOS: %s %s" %(words[0], words[2], platform.system(), os.name)
	s.connect((words[2], tport))
	s.send(msg)
	msg = s.recv(1024)
	print msg
	s.close()
	#thread = myThread("reqfrompeer",sock=s, msg = msg)
	#thread.start()
	

main()
		
		
		
		
		
		
		
'''
	if(count%100000==0):
		print s.recv(1024)
	count+=1
	'''
'''
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((socket.gethostbyname(msg[0]) , msg[1]))
s1.listen(5)

while True:
	client,addr = s1.accept()
	client.send("Msg from Client")
	client.close()
#s.close()
'''


""" TODO:



"""