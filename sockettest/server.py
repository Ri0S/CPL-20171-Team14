from socket import*

PORT = 12345
BUFSIZE = 512
HOST = '127.0.0.1'
ADDR = (HOST, PORT)
servSocket = socket(AF_INET, SOCK_STREAM)

servSocket.bind(ADDR)
servSocket.listen(5)
clntSocket, addr_info = servSocket.accept()

while(1):
	clntbuf = clntSocket.recv(BUFSIZE)
	clntSocket.send("3")

clntSocket.close()
servSocket.close()
