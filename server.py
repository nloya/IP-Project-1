import socket
import pickle
import threading

lock = threading.Lock()
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
	
	@staticmethod	
	def remRFC(host, port):		#l[:] = [tl for tl in l if tl>16]
		for r in rfc:
			r.hostportlist[:] = [hp for hp in r.hostportlist if hp.host!=host or hp.port!=port]          


class myThread (threading.Thread):
	def __init__(self, client, addr):
		threading.Thread.__init__(self)
		self.client = client # 
		self.addr = addr # ('169.254.96.162', 57761)
		
	
	def run(self):		
		host =""
		port = ""
		while True:
			try:
				msg = self.client.recv(1024)
				#print ("Message: %s" %msg)
				msg = msg.decode('UTF-8')
				#print ("Message: %s" %msg)
				line = msg.split('\n')
				#print("Line: %s" %line)
				word = line[0].split(' ')
				host = line[1].split(' ')[1]			
				port = line[2].split(' ')[1]
				if(word[0]=='ADD'):
					rfcno = word[2]					
					title = line[3].split(' ')[1]
					print("\n%s %s %s %s" %(rfcno,host,port,title))
					#p = Peers(host,port)
					lock.acquire()
					Peers.addPeer(host,port) # adds only if the peer is not already present
					#displayPeer()
					RFC.addRFC(rfcno,title,host,port)
					lock.release()
					#displayRFC()
					#print("Message: %s" %len(msg))
					tmpmsg = "P2P-CI/1.0 200 OK\nRFC %s %s %s %s" %(rfcno,title,host,port)
					self.client.send(bytes(tmpmsg, 'UTF-8'))
				elif(word[0]=='LOOKUP'):
					rfcno = word[2]
					title = line[3].split(' ')[1]
					flag = False
					tempmsg = ""
					lock.acquire()
					for r in rfc:
						if r.rfcno == rfcno and r.title == title:
							flag = True
							for hp in r.hostportlist:
								tempmsg += ("%s %s %s %s\n" %(r.rfcno,r.title,hp.host,hp.port))
					lock.release()
					tempmsg.strip()
					if flag:
						tmpmsg = "P2P-CI/1.0 200 OK\n%s" %tempmsg
						self.client.send(bytes(tmpmsg,'UTF-8'))
					else:
						tmpmsg = "P2P-CI/1.0 404 Not Found\n"
						self.client.send(bytes(tmpmsg,'UTF-8'))
				elif(word[0]=='LIST'):
					tempmsg = ""
					lock.acquire()
					for r in rfc:
						for hp in r.hostportlist:
							tempmsg += ("%s %s %s %s\n" %(r.rfcno,r.title,hp.host,hp.port))
					lock.release()
					displayRFC()
					tempmsg.strip()
					tmpmsg = "P2P-CI/1.0 200 OK\n%s" %tempmsg
					print(tmpmsg)
					self.client.send(bytes(tmpmsg,'UTF-8'))			
			except Exception as e:
				print(self.addr[0] + "  Client ends connection  " + str(self.addr[1]))
				#print(host + "  Client ends connection  " + port)   
				displayRFC()
				print(host + "  Client's Upload Server also goes down  " + port)
				RFC.remRFC(host, port)
				displayRFC()
				self.client.close()
				break
			


def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print(s)
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
		print('*'*40)
		print(client)
		print(addr)
		print('*'*40)
		thread = myThread(client, addr)
		thread.start()		
	
main()
