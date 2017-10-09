#CS.py
import socket
import sys
import errno
import os
import time
import struct


tasks = []
numRequest = '0001'
numWS = '001'

# reading arguments
if len(sys.argv) == 1:
	CSport = 58011

else: 
	CSport = int(sys.argv[2])



CSHostName = socket.gethostname()	 

def writeInFile():

	print(len(lrequest[3]))
	x = 8 + len(lrequest[3])
	filename = open(numRequest + ".txt", "w")
	for i in range(x, len(request), 1):
		filename.write(request[i]) 

def putInFile(task, IPWS, portWS):

	filename = open("file_processing_tasks.txt", "a")
	filename.write(task + ' ' + IPWS + ' ' + str(portWS) + '\n')
	filename.close()

def removeFile(task,IPWS, portWS):

	verif = False
	filename = open("file_processing_tasks.txt", "r")
	resto = ''
	
	for lines in filename:
		line = lines.split()
		if line != []:
			if line[1] != str(IPWS) or line[0] != task or line[2] != str(portWS):
					resto = resto + lines
			else:
				print '-' + task + ' ' + IPWS + ' ' + str(portWS) + '\n'
				verif = True	
	filename.close()

	filename = open("file_processing_tasks.txt", "w")
	filename.write(resto)	
	filename.close()
	return verif
	

def getIPWS():

	filename = open("file_processing_tasks.txt", "r")

	for lines in filename:
		line = lines.split()
		return line[1]

def getportWS():

	filename = open("file_processing_tasks.txt", "r")

	for lines in filename:
		line = lines.split()
		return line[2]
		


def WS():

	s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
	s_udp.bind((CSHostName, CSport))

	while True:

		message, addr = s_udp.recvfrom(1024)
		messages = message.split()

		if messages[0] == 'REG': # adding a new WS
			IPWS = messages[-2]
			portWS = messages[-1]

			answer = ''

			if addr[1] < 49151 or addr[1] > 65535 or int(portWS) < 49151 or int(portWS) > 65535:
				answer = 'RAK NOK\n'
				print "ERROR_PORT: Port number is out of range"
				try:
					s_udp.sendto(answer, addr)

				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to WS"
					print senderror
						  		

				
			if addr[0] != IPWS:
				answer = 'RAK NOK\n'
				print "IP_ERROR: Incorrect IP"
				try:
					s_udp.sendto(answer, addr)

				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to WS"
					print senderror
						 	
	 
			elif answer == '': # otherwise, add to list
	
				answer = 'RAK OK\n'
				try:
					s_udp.sendto(answer, addr)
					i = 1
					while(i < len(messages) -2):
						print '+' + messages[i] + ' ' + IPWS + ' ' + str(portWS) 
						print('\n')
						putInFile(messages[i], IPWS, portWS)
						i = i + 1 

				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to WS"
					print senderror
						 		

			

			"""else: # wrong syntax
				answer = 'RAK ERR\n'
				print "ARGS_ERROR: Number of arguments are not valid"
				try:
					s_udp.sendto(answer, addr)
				except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to WS"
						print senderror"""
			
			messages = ()				 				


		elif messages[0] == 'UNR': # closing the WS

			IPWS = messages[-2]
			portWS = messages[-1]

			answer = ''
			removeAccepted = False
			
			try:
				
				i = 1
				while(i < len(messages) -2 ):
					taskRemoved = removeFile(messages[i], IPWS, portWS)
					if(removeAccepted == False and taskRemoved == True):
						removeAccepted = True
						answer = 'UAK OK\n'
						s_udp.sendto(answer, addr)
					
					i = i + 1

			except socket.error as senderror:
				if(senderror.errno != errno.ECONNREFUSED):
					raise senderror
				print "SOCKET_ERROR: Error sending message to WS"
				print senderror
							 					
			if answer == '':
				answer = 'UAK NOK\n'
				print "WS_ERROR: WS not found in processing_tasks"
				try:
					s_udp.sendto(answer, addr)

				except socket.error as senderror:
					if(senderror.errno != errno.ECONNREFUSED):
						raise senderror
					print "SOCKET_ERROR: Error sending message to WS"
					print senderror
						 			

					
				
			"""else: # wrong syntax
				answer = 'UAK ERR\n'
				print "ARGS_ERROR: Number of arguments are not valid"
				try:
					s_udp.sendto(answer, addr)
				except socket.error as senderror:
						if(senderror.errno != errno.ECONNREFUSED):
							raise senderror
						print "SOCKET_ERROR: Error sending message to WS"
						print senderror"""
						 				
		
	os._exit(0)


	

	
while True:
	
	
	newpid = os.fork()
	if newpid == 0:
		WS()  
	elif newpid > 0:

		s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
		s_tcp.bind((CSHostName, CSport))	
	
		while True:
			
			s_tcp.listen(5) # 	waits for users
			connection, address = s_tcp.accept()

			request = connection.recv(2048)
			lrequest = request.split()

				
			if request == "LST\n":
				
				
				answer = ''
				
				filename = open("file_processing_tasks.txt", "r")

				filename.seek(0)
				first_char = filename.read(1)
				if not first_char:
					answer = ' '
		 		else:
					
					filename.seek(0)
					x = 1 
					for lines in filename:
						line = lines.split()
						
						if line[0] == "WCT":
							answer = answer +  str(x) + '-' + ' ' + 'WCT' + ' ' + '-' + ' ' + 'word count\n'
						elif line[0] == "FLW":
							answer = answer +  str(x) +  '-' + ' ' + 'FLW' + ' ' + '-' + ' ' + 'find longest word\n'	
						elif line[0] == "UPP":
							answer = answer + str(x) +  '-' + ' ' + 'UPP' + ' ' + '-' + ' ' + 'convert text to upper case\n'	
						elif line[0] == "LOW":
							answer = answer + str(x) +  '-' + ' ' + 'LOW' + ' ' + '-' + ' ' + 'convert text to lower case\n'	
						else:
							print "TASK_ERROR: Unrecognizable task"
							answer = "TASK_ERROR: Unrecognizable task"	

						x += 1

						
				connection.sendall(answer)	

				request = connection.recv(1024)

				print(request)

				connection.close()

			elif lrequest[0] == "REQ":

				print(request)

				writeInFile()

				IPWS = getIPWS()
				portWS = getportWS()
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
				sock.connect((IPWS,int(portWS)))
				answer = "WRQ" + ' ' + lrequest[1] + ' ' + numRequest + numWS + ".txt" +  ' ' +  lrequest[2] + ' ' + '\n'   
				sock.send(answer)
				sock.close()	
				print(request)




	else: 
			
		print "PROCESS_ERROR: Fork error"			

			

			
			#connection.sendall(request)
			#connection.close()

			
		# CS - user 








	