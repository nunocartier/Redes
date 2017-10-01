#user.py
import socket
import sys

CSHostName = socket.gethostname()
CSport = 58011

for i in range (1, len(sys.argv), 2):

	if sys.argv[i] == "-n":
		CSHostName = sys.argv[i+1]
		continue
	elif sys.argv[i] == "-p":
		CSport = int(sys.argv[i+1])
		continue

while True:
	
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP SOCKET
	sock.connect((CSHostName,CSport)) # user connection [TCP]
	print("CS host: ", CSHostName, "CS port: ", CSport)

	sys.stdout.write('> ')
	sys.stdout.flush()
	command_line = raw_input()

	#list
	if command_line == "list":

		sock.send("LST\n")


	#if command_line == "request":	



	#exit
	if command_line == "exit":

		sock.close()
		sys.exit()
