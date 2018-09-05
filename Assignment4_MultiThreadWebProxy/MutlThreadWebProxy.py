#!/usr/bin/env python
from socket import *
import thread

class ConstantVar(object):
	# Http format info
	__sp = ' '
	__crlf = '\r\n'
	__colon = ':'

	# response line
	__version = 'HTTP/1.1'
	__statusOK = '200'
	__statusErrInvalidMethod = '405'
	__phraseOK = 'OK'
	__phraseErrInvalidMethod = 'Not Allowed Method'

	# header line
	__contentTypeName = 'Content-Type'
	__contentTypeValue = 'test/html'

	# Proxy server info
	proxyPort = 8000
	maxLength = 1024

	def buildHeaderLine(name, value):
    	return name + __colon + __sp + value + __crlf

class HttpRequest(object):
	def __init__(self, requestMessage):
        # request message includes request line, header lines, blank line, entity body
        self.__lines = requestMessage.split(sep=ConstantVar.__crlf)

        # fileds of request line
        self.__requestLineFields = self.__lines[0].split(sep=ConstantVar.__sp)

    def getMethod(self):
    	return self.__requestLineFields[0]

    def getUrl(self):
        return self.__requestLineFields[1]

class HttpResponse(self):
	def __init__(self):
		# fields of status line
        self.__version = ConstantVar.__version
        self.__status = ConstantVar.__statusOK
        self.__phrase = ConstantVar.__phraseOK

        # fileds of header lines
        self.__contentTypeName = ConstantVar.__contentTypeName
        self.__contentTypeValue = ConstantVar.__contentTypeValue

        # entity body
        self.__entityBody = ''

    def setStatusLine(self, version, status, phrase):
        self.__version = version
        self.__status = status
        self.__phrase = phrase

    def setEntityBody(self, data):
        self.__entityBody = data

    def getMessage(self):
        statusLine = self.__version + ConstantVar.__sp + self.__status + ConstantVar.__sp + self.__phrase + ConstantVar.__crlf

        contentTypeLine = ConstantVar.buildHeaderLine(self.__contentTypeName,self.__contentTypeValue)
        headerLines = contentTypeLine

        blankLine = ConstantVar.__crlf

        return statusLine + headerLines + blankLine + self.__entityBody

class WebProxy(object):

	def __init__(self, port):
		self.__port = port
		self.__socket = socket(AF_INET, SOCK_STREAM)

	def __proxyFunc(connSocket, connAddr):
		try:
			recvMessageBytes = connSocket.recv(ConstantVar.maxLength)
			recvMessage = recvMessageBytes.decode('utf-8')

			httpRequest = HttpRequest(recvMessage)
			method = httpRequest.getMethod()

			if method == 'GET':

			else:
				
		except Exception as e:
			print(e)
		finally:
			connSocket.close()

	def start(self):
		self.__socket.bind(('',self.__port))
		self.__socket.listen(1)
		while True:
			connSocket, connAddr = self.__socket.accept()
			thread.start_new_thread(WebProxy.__proxyFunc, (connSocket, connAddr))

	def end(self):
		self.__socket.close()