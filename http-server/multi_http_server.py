import time
from socket import *
import sys # to terminate the program
import threading


def handleRequest(connectionSocket):
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


serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverPort = 11000
serverSocket.bind(('',serverPort))
serverSocket.listen(5)
print('ready to recieve')


while True:
    print(threading.active_count())
    connectionSocket,client_addr = serverSocket.accept()
    print('Got connection from',client_addr,'\n')
    threading.Thread(target=handleRequest,args=(connectionSocket,)).start()



# serverSocket.close()
# sys.exit() #terminating the program after sending the corresponding data