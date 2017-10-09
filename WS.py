#WS.py
from collections import Counter
import sys 
import socket 
import os 
import signal
import time


task = []
WSport = 59000
CSHostname = socket.gethostname()
CSport = 58011




# reading arguments
for i in range(1, len(sys.argv), 2): 
	if sys.argv[i] == '-p':
		WSport = int(sys.argv[i+1])
		continue
	elif sys.argv[i] == '-n':
		CSHostname = sys.argv[i+1]
		continue
	elif sys.argv[i] == '-e':
		CSport = int(sys.argv[i+1])
		continue

def putTask():
	l = 1
	while(l != len(sys.argv)):
		if(sys.argv[l] == "WCT" or sys.argv[l] == "FLW" or sys.argv[l] == "UPP" or sys.argv[l] == "LOW"): 
			task.append(sys.argv[l])
		l = l + 1	 	

def WCT(filename):

	fle = open(filename, "r")
	
	wordCount = Counter(fle.read().split())

	return wordCount

def FLW(filename):
	
	fle = open(filename, "r")

	stringsplit = fle.read().split()


	longestWord = max(stringsplit, key=len)


def UPP(filename):

	fle = open(filename, "r+b")

	content = fle.read()

	fle.seek(0)
	fle.write(content.upper())


def LOW(filename):

	fle = open(filename, "r+b")

	content = fle.read()

	fle.seek(0)
	fle.write(content.lower())


			


print("CS host: ", CSHostname, "CS port: ", CSport, "WS port:", WSport)	


#registo (UDP)

try:

	s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s_tcp.bind((socket.gethostbyname(socket.gethostname()), WSport))	
	s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  

	i = 0
	putTask()
	answer = 'REG '
	while(i < len(task)):
		answer = answer + task[i] + ' '
		i = i + 1

	answer = answer + str(socket.gethostbyname(socket.gethostname())) + ' ' + str(WSport) 
	print(answer)
	s_udp.sendto(answer,(CSHostname, CSport))

	message, addr = s_udp.recvfrom(1024)
	messages = message.split() # gets answer from CS 
		
	if messages[0] == 'RAK':
		if messages[1] == 'NOK\n': 
			print 'Dolorosamente houve, devido a certas circunstancias, um problema que nao permitiu o registo do WS no CS'
			sys.exit(0)


	while True: 

		s_tcp.listen(5) # 	waits for users
		connection, address = s_tcp.accept()

		newpid = os.fork()
		if newpid == 0:
			
			request = connection.recv(2048)
			lrequest = request.split()
			print(request)

			if lrequest[1] == 'WCT' or lrequest[1] == 'FLW' or lrequest[1] == "UPP" or lrequest[1] == 'LOW':
				
			
			else:
			
				connection.sendall("REP EOF")
				connection.close()

		


except KeyboardInterrupt:

	try:
		i = 0
		answer = 'UNR '
		while(i < len(task)):
			answer = answer + task[i] + ' '
			i = i + 1

		answer = answer + ' ' + str(socket.gethostbyname(socket.gethostname())) + ' ' + str(WSport) 
		print(answer)
		s_udp.sendto(answer,(CSHostname, CSport))


	except socket.error as senderror:
		if(senderror.errno != errno.ECONNREFUSED):
			raise senderror
		print "SOCKET_ERROR: Error sending message to WS"
		print senderror
		
	message, addr = s_udp.recvfrom(2100)
	messages = message.split()	


	if messages[0] == 'UAK':
		if messages[1] == 'NOK\n' or messages[1] == 'ERR\n':
			print(messages[1])
			print 'problema ao anular o registo'
			sys.exit(0)
		if messages[1] == 'OK\n':
			s_udp.close()
			print 'exit'
			sys.exit(0)





#print("CS host: ", CSHostName, "CS port: ", CSport, "WS port:", WSport)		


