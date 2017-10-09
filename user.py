#user.py
import socket
import sys
import os

CSHostName = socket.gethostname()
CSport = 58011




# reading arguments
for i in range (1, len(sys.argv), 2):

	if sys.argv[i] == "-n":
		CSHostName = sys.argv[i+1]
		continue
	elif sys.argv[i] == "-p":
		CSport = int(sys.argv[i+1])
		continue




# Funcoes ---------------------------------------

def connect():

	sock.connect((CSHostName,CSport)) # user connection [TCP]	

def disconnect():

	sock.close()

def  userClose():

	sock.close()
	sys.exit()	

def getSize(filename):
    st = os.stat(filename)
    return st.st_size	

# -----------------------------------------------


while True:
	
	lAnswer = []

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP SOCKET
	
	print("CS host: ", CSHostName, "CS port: ", CSport)

	sys.stdout.write('> ')
	sys.stdout.flush()
	command_line = raw_input()

	lcommand_line = command_line.split()
	if command_line == "list":

		tasks = []

		connect()
		sock.send("LST\n")

		answer = sock.recv(1024)
		lAnswer = answer.split()

		print(answer)
		
		if lAnswer == []:
			sock.send("FPT EOF")
		elif(lAnswer[0] == "TASK_ERROR: Unrecognizable task"):
			sock.send("FPT ERR")	

		else:	

			num = 0	
			answer = ''
			for i in range(1, len(lAnswer), 1):
				if(lAnswer[i] == "WCT" or lAnswer[i] == "FLW" or lAnswer[i] == "UPP" or lAnswer[i] == "LOW"):
					tasks.append(lAnswer[i])
					answer = answer + lAnswer[i] + ' '
					num += 1

			answer = "FPT" + ' ' + str(num) + ' ' + answer
			sock.send(answer)		 
				 

		disconnect()


	elif lcommand_line[0] == "request":

		if(len(lcommand_line) == 3): 
			if(lcommand_line[1] == "WCT" or lcommand_line[1] == "FLW" or lcommand_line[1] == "LOW" or lcommand_line[1] == "UPP"):
				f = open(lcommand_line[2], 'rb')
				size = getSize(lcommand_line[2])
				dat = f.read(size) 


				answer = "REQ" + ' ' + lcommand_line[1] +  ' ' + str(size) + ' ' + str(dat) + '\n' 
				connect()
				sock.send(answer)	




	#if command_line == "request":	



	#exit
	elif command_line == "exit":

		userClose()
		
	