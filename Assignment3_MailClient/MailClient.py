#!/usr/bin/env python
from socket import *
import os
import sys
import base64

# Constant Var of HTTP format
sp = ' '
crlf = '\r\n'
hello = "HELO"
auth = "AUTH LOGIN"
mailfrom = "MAIL FROM"
rcptto = "RCPT TO"
data = "DATA"
colon = ':'
quit = "QUIT"
ending = '.'

# Mail info
myUsername = "shengsiyuan"
myHostname = "ict.ac.cn"
targetUsername = sys.argv[2]
targetHostname = sys.argv[3]
loginName = sys.argv[4]
loginPasswd = sys.argv[5]

# Server info
serverIP = sys.argv[1]
serverPort = 25
maxLength = 1024

def bulidCmdBytes(name, value):
	return (name + sp + value + crlf).encode('utf-8')

def buildCmdWithColonBytes(name, value):
	return (name + colon + sp + value + crlf).encode('utf-8')

def buildContactString(name, host):
    return '<' + name + '@' + host + '>'

clientSocket = socket(family=AF_INET, type=SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))

try:
	# SMTP handshaking
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send(bulidCmdBytes(hello, myHostname))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send(buildCmdWithColonBytes(mailfrom, buildContactString(myUsername, myHostname)))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send((auth+crlf).encode("utf-8"))
	# there is an error
	clientSocket.send(base64.b64encode(loginName+crlf).encode("utf-8"))
	clientSocket.send(base64.b64encode(loginPasswd+crlf).encode("utf-8"))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send(buildCmdWithColonBytes(rcptto, buildContactString(targetUsername, targetHostname)))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send((data+crlf).encode("utf-8"))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	message = ""
	while(True):
		tempLine = sys.stdin.readline().strip('\n')
		if tempLine != quit:
			message = message + tempLine + crlf
		else:
			message = message + ending + crlf
			break
	clientSocket.send(message.encode("utf-8"))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send((quit+crlf).encode("utf-8"))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))
except Exception as e:
    print(str(e))
finally:
    clientSocket.close()



