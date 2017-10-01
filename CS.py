#CS.py
import socket
import sys



if len(sys.argv) == 1:
	CSport = 58011

else: 
	CSport = int(sys.argv[2])


#print("CS host: ", CSHostName, "CS port: ", CSport)

CSHostName = socket.gethostname()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
sock.bind((CSHostName, CSport))
processing_tasks = []

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
s_tcp.bind((CSHostName, CSport))



def retList(connection):

	print(request)
	#fazer coisas 
	
while True:
	
	message, addr = sock.recvfrom(1024)
	print(message)
	messages = message.split()

	if messages[0] == 'REG': # adding a new WS
		if len(messages) == 4:
			task = messages[1]
			IPWS = messages[2]
			portWS = messages[3]

			answer = ''
			
			for i in processing_tasks:
				if i[0] == task: # task already has a dedicated ws 
					answer = 'RAK NOK\n'
					sock.sendto(answer, addr)
					break

			if answer == '': # otherwise, add to list
				processing_tasks.append([task,(IPWS,portWS)])
				answer = 'RAK OK\n'
				sock.sendto(answer, addr)
				print '+' + task + ' ' + IPWS + ' ' + str(portWS)
				print(processing_tasks[0])
				
		"""else: # wrong syntax
			answer = 'RAK ERR\n'
			sock.sendto(answer, addr)"""	

	

	# CS - user 

	
	s_tcp.listen(5) # waits for users
	connection, address = s_tcp.accept()
	request = connection.recv(5)
	lrequest = request.split()
	
	
	if request == "LST\n":
		retList(connection)

	

	
	#connection.sendall(answer)
	connection.close()




	