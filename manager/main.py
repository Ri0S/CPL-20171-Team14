from socket import*

PINSET_MODE = 0
MODESET_MODE = 1
REQUEST = 2

serverName = "192.168.0.2"
serverPort = 12345

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.bind((serverName, 0))

clientSocket.connect((serverName, serverPort))

clientSocket.send()
clientSocket.recv()

clientSocket.close()

