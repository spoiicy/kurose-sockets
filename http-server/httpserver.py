import time
from socket import *
import sys # to terminate the program

serverSocket = socket(AF_INET,SOCK_STREAM)
serverPort = 11000
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

while True:
    print('ready to recieve')
    connectionSocket, client_addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines()
        statusline = "HTTP/1.1 200 OK\r\n"
        connectionSocket.send(statusline.encode())
        connectionSocket.send("\r\n".encode())
        for i in range(0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
        error_header = "HTTP/1.1 404 Not Found\r\n"
        connectionSocket.send(error_header.encode())
        connectionSocket.send("\r\n".encode())
        
        # ferr = open('error.html')
        # output = ferr.read()
        # print(output)
        # connectionSocket.send(output.encode())
        error_message = "<!DOCTYPE html><html><head><title>Error</title></head><body><h1>404 Not Found</h1></body></html>"
        connectionSocket.send(error_message.encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    time.sleep(10)
    
serverSocket.close()
sys.exit() #terminating the program after sending the corresponding data