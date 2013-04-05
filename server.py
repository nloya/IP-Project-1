import socket
import pickle
import threading

peerlist = list()
rfc = list()

def displayPeer():
	for p in peerlist:
		print("P: %s %s" %(p.host,p.port))

def displayRFC():
	for r in rfc:
		for hp in r.hostportlist:
			print("R: %s %s %s %s" %(r.rfcno,r.title,hp.host,hp.port))

class Peers():
	def __init__(self,host,port):
		self.host = host
		self.port = port

	@staticmethod
	def addPeer(host,port):
		for p in peerlist:
			if p.host == host and p.port == port:				
				return
		peerlist.append(Peers(host,port))

class RFC():
	def __init__(self,rfcno,title,host,port):
		self.rfcno = rfcno
		self.title = title
		self.hostportlist = list()
		self.hostportlist.append(Peers(host,port))
	
	@staticmethod
	def addRFC(rfcno,title,host,port):
		for r in rfc:
			if r.rfcno == rfcno:
				for hp in r.hostportlist:
					if hp.host == host and hp.port == port:
						return				
				r.hostportlist.append(Peers(host,port))
				return
		rfc.append(RFC(rfcno,title,host,port))
                


class myThread (threading.Thread):
	def __init__(self, client, addr):
		self.client = client
		self.addr = addr
		threading.Thread.__init__(self)
	
	def run(self):
		#self.client.send("Thank you for connecting")
		while(True):
			#self.client.send("Thank you for connecting")
			msg = self.client.recv(1024)
			#print msg		
			line = msg.split('\n')
			word = line[0].split(' ') 
			if(cmp(word[0],'ADD')==0):
				rfcno = word[2]
				host = line[1].split(' ')[1]
				port = line[2].split(' ')[1]
				title = line[3].split(' ')[1]
				print("\n%s %s %s %s" %(rfcno,host,port,title))
				#p = Peers(host,port)
				Peers.addPeer(host,port) # adds only if the peer is not already present
				displayPeer()
				RFC.addRFC(rfcno,title,host,port)
				displayRFC()
				#print("Message: %s" %len(msg))
				self.client.send("P2P-CI/1.0 200 OK\nRFC %s %s %s %s" %(rfcno,title,host,port))
			elif(cmp(word[0],'LOOKUP')==0):
				rfcno = word[2]
				title = line[3].split(' ')[1]
				flag = False
				tempmsg = ""
				for r in rfc:
					if r.rfcno == rfcno and r.title == title:
						flag = True
						for hp in r.hostportlist:
							tempmsg += ("%s %s %s %s\n" %(r.rfcno,r.title,hp.host,hp.port))
				if flag:
					self.client.send("P2P-CI/1.0 200 OK\n%s" %tempmsg)
				else:
					self.client.send("P2P-CI/1.0 404 Not Found\n")
			elif(cmp(word[0],'LIST')==0):
				tempmsg = ""
				for r in rfc:
					for hp in r.hostportlist:
						tempmsg += ("%s %s %s %s\n" %(r.rfcno,r.title,hp.host,hp.port))
				self.client.send("P2P-CI/1.0 200 OK\n%s" %tempmsg)
		self.client.close()
		



def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
