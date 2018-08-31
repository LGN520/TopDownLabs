#!/usr/bin/env python
from socket import *
import os
import sys
import base64

# Actually the SMTP we implemented is ESMTP

class SMTP(object):

	# Constant Var of SMTP format
	__sp = ' '
	__crlf = '\r\n'
	__hello = "EHLO"
	__authplain = "AUTH PLAIN"
	__authlogin = "AUTH LOGIN"
	__user = "USER"
	__passwd = "PASS"
	__mailfrom = "MAIL FROM"
	__rcptto = "RCPT TO"
	__data = "DATA"
	__colon = ':'
	__quit = "QUIT"
	__ending = '.'
	__null = '\0'

	def __init__(self, serverIP, targetAddress, loginName, loginPasswd):
		# Mail info
		self.myHostname = "ssy"
		self.myAddress = loginName
		self.targetAddress = targetAddress
		self.loginName = loginName
		self.loginPasswd = loginPasswd

		# Server info
		self.serverIP = serverIP
		self.serverPort = 25
		self.maxLength = 1024

	def buildKVCmdBytes(name, value):
		return (name + SMTP.__sp + value + SMTP.__crlf).encode('utf-8')

	def buildCmdBytes(name):
		return (name + SMTP.__crlf).encode('utf-8')

	def buildKVCmdWithColonBytes(name, value):
		return (name + SMTP.__colon + SMTP.__sp + value + SMTP.__crlf).encode('utf-8')

	def buildContactString(mailAddress):
   		return '<' + mailAddress + '>'

	def buildLoginB64(value):
   		return base64.b64encode(value.encode('utf-8')) + b'\r\n'

	def buildPlainB64(username, passwd):
		return base64.b64encode((SMTP.__null+username+SMTP.__null+passwd).encode('utf-8')) + b'\r\n'

	def base64Decode(base64Bytes, encodingType = 'utf-8'):
		paddingNum = 4 - len(base64Bytes)%4
		base64Bytes += b'='*paddingNum
		return base64.b64decode(base64Bytes).decode(encodingType)

	def __del__(self):
		self.clientSocket.close()

	def begin(self):
		# Client socket
		self.clientSocket = socket(family=AF_INET, type=SOCK_STREAM)
		self.clientSocket.connect((self.serverIP,self.serverPort))

		# recv 220 from server
		print("SMTP handshaking starts...")
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

	def ehlo(self):
		# hello
		print("Hello...")
		self.clientSocket.send(SMTP.buildKVCmdBytes(SMTP.__hello, self.myHostname))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

	def authPlain(self):
		# auth plain
		print("Auth plain...")
		self.clientSocket.send(SMTP.buildCmdBytes(SMTP.__authplain))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

		print("Send username and passwd...")
		self.clientSocket.send(SMTP.buildPlainB64(self.loginName, self.loginPasswd))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

	def authLogin(self):
		# auth login
		print("Auth...")
		self.clientSocket.send(SMTP.buildCmdBytes(SMTP.__authlogin))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		base64Str = SMTP.base64Decode(recvMessageBytes[4:-2])
		print("Base64 decode result:\r\n" + base64Str) # username:
		print(recvMessageBytes.decode('utf-8'))
		
		print("Send username...")
		self.clientSocket.send(SMTP.buildLoginB64(self.loginName))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		base64Str = SMTP.base64Decode(recvMessageBytes[4:-2])
		print("Base64 decode result:\r\n" + base64Str) # Passwd:
		print(recvMessageBytes.decode('utf-8'))

		print("Send passwd...")
		self.clientSocket.send(SMTP.buildLoginB64(self.loginPasswd))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

	def mailfrom(self):
		# mail from
		print("Mail from...")
		self.clientSocket.send(SMTP.buildKVCmdWithColonBytes(SMTP.__mailfrom, SMTP.buildContactString(self.myAddress)))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

	def rcptto(self):
		# rcpt to
		print("Rcpt to...")
		self.clientSocket.send(SMTP.buildKVCmdWithColonBytes(SMTP.__rcptto, SMTP.buildContactString(self.targetAddress)))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

	def sendMessage(self):
		self.clientSocket.send(SMTP.buildCmdBytes(SMTP.__data))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

		message = ""
		while(True):
			tempLine = sys.stdin.readline().strip('\n')
			if tempLine != SMTP.__quit:
				message = message + tempLine + SMTP.__crlf
			else:
				message = message + SMTP.__ending + SMTP.__crlf
				break
		self.clientSocket.send(message.encode("utf-8"))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

		self.clientSocket.send(SMTP.buildCmdBytes(SMTP.__quit))
		recvMessageBytes = self.clientSocket.recv(self.maxLength)
		print(recvMessageBytes.decode('utf-8'))

		del(self)

try:
	# SMTP handshaking
	mysmtp = SMTP(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

	mysmtp.begin()

	mysmtp.ehlo()

	#mysmtp.authPlain()
	mysmtp.authLogin()

	mysmtp.mailfrom()

	mysmtp.rcptto()

	mysmtp.sendMessage()
 
	# there are 3 main auth alternatives: LOGIN, PLAIN and CRAM-MD5
	# we use LOGIN here


except Exception as e:
    print(str(e))



