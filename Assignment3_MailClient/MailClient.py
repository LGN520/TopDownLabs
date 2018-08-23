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
user = "USER"
passwd = "PASS"
mailfrom = "MAIL FROM"
rcptto = "RCPT TO"
data = "DATA"
colon = ':'
quit = "QUIT"
ending = '.'

# Mail info
myHostname = "ict.ac.cn"
myMailAddress = "shengsiyuan@ict.ac.cn"
targetmailAddress = sys.argv[2]
loginName = sys.argv[3]
loginPasswd = sys.argv[4]

# Server info
serverIP = sys.argv[1]
serverPort = 25
maxLength = 1024

def bulidKVCmdBytes(name, value):
	return (name + sp + value + crlf).encode('utf-8')

def buildCmdBytes(name):
		return (name + crlf).encode('utf-8')

def buildKVCmdWithColonBytes(name, value):
	return (name + colon + sp + value + crlf).encode('utf-8')

def buildContactString(mailAddress):
    return '<' + mailAddress + '>'

clientSocket = socket(family=AF_INET, type=SOCK_STREAM)
clientSocket.connect((serverIP,serverPort))

try:
	# SMTP handshaking
	# recv 220 from server
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	# hello
	clientSocket.send(bulidKVCmdBytes(hello, myHostname))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	# auth login
	clientSocket.send((auth+crlf).encode("utf-8"))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))
	
	clientSocket.send(base64.b64encode(buildCmdBytes(loginName)))

	clientSocket.send(base64.b64encode(buildCmdBytes(loginPasswd)))
	# recvMessageBytes = clientSocket.recv(maxLength)
	# print(recvMessageBytes.decode('utf-8'))

	# send from
	clientSocket.send(buildKVCmdWithColonBytes(mailfrom, buildContactString(myMailAddress)))
	recvMessageBytes = clientSocket.recv(maxLength)
	print(recvMessageBytes.decode('utf-8'))

	clientSocket.send(buildKVCmdWithColonBytes(rcptto, buildContactString(targetmailAddress)))
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



