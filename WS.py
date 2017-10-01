#WS.py
import sys 
import socket 
import os 
import signal


task = sys.argv[1]
WSport = 59000
CSHostname = socket.gethostname()
CSport = 58011

# reading arguments
for i in range(2, len(sys.argv), 2): 
	if sys.argv[i] == '-p':
		WSport = int(sys.argv[i+1])
		continue
	elif sys.argv[i] == '-n':
		CSHostname = sys.argv[i+1]
		continue
	elif sys.argv[i] == '-e':
		CSport = sys.argv[i+1]
		continue

print("CS host: ", CSHostname, "CS port: ", CSport, "WS port:", WSport)	


#registo (UDP)

try:

	s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#s_udp.connect((CSHostname, CSport))
	print("coco")    

	answer = 'REG ' + task + ' ' + str(socket.gethostbyname(socket.gethostname())) + ' ' + str(CSport)
	s_udp.sendto(answer, (CSHostname, CSport))

	message, addr = s_udp.recvfrom(1024)
	messages = message.split() # gets answer from CS 
	print(message)
	
	if messages[0] == 'RAK':
		if messages[1] == 'NOK': 
			print 'RAK ERR'
			sys.exit(0)

			#O CS tem que responder alguma coisa ao WS quando este se regista
		
except KeyboardInterrupt:

	print("coco")

while True:

	x = 0



#print("CS host: ", CSHostName, "CS port: ", CSport, "WS port:", WSport)		


