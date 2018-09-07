#!/usr/bin/env python
from socket import *
import os

# Constant Var of HTTP format
sp = ' '
crlf = '\r\n'
colon = ':'
version = 'HTTP/1.1'
statusOK = '200'
statusErr = '404'
phraseOK = 'OK'
phraseErr = 'Not Found'

# Server info
serverPort = 80
maxLength = 1024
basePath = os.path.abspath('')

def buildHeaderLine(name, value):
    return name + colon + sp + value + crlf

# Http Request
class HttpRequest(object):
    __test = 1

    def __init__(self, requestMessage):
        # request message includes request line, header lines, blank line, entity body
        self.__lines = requestMessage.split(sep=crlf)

        # fileds of request line
        self.__requestLineFields = self.__lines[0].split(sep=sp)
        print(self.__requestLineFields)

    def getUrl(self):
        urlLine = self.__requestLineFields[1]
        index = urlLine.find("localhost")
        if index >= 0:
    	    urlLine = urlLine[index+len("localhost"):]
        return urlLine

# Http Response(object)
class HttpResponse(object):
    def __init__(self):
        # fields of status line
        self.__version = version
        self.__status = statusOK
        self.__phrase = phraseOK

        # fileds of header lines
        self.__contentTypeName = 'Content-Type'
        self.__contentTypeValue = 'text/html'

        # entity body
        self.__entityBody = ''

    def setStatusLine(self, version, status, phrase):
        self.__version = version
        self.__status = status
        self.__phrase = phrase

    def setEntityBody(self, data):
        self.__entityBody = data

    def getMessage(self):
        statusLine = self.__version + sp + self.__status + sp + self.__phrase + crlf

        contentTypeLine = buildHeaderLine(self.__contentTypeName,self.__contentTypeValue)
        headerLines = contentTypeLine

        blankLine = crlf

        return statusLine + headerLines + blankLine + self.__entityBody

serverSocket = socket(family=AF_INET, type=SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
while(True):
    connectionSocket, clientAddr = serverSocket.accept()
    requestMessageBytes = connectionSocket.recv(maxLength)
    httpRequest = HttpRequest(requestMessageBytes.decode('utf-8'))
    httpResponse = HttpResponse()
    try:
        # get url (filename)
        filename = basePath + httpRequest.getUrl()
        print(filename)
        # get file content
        fd = open(filename, 'r')
        filedata = fd.read()
        fd.close()
    except IOError:
        httpResponse.setStatusLine(version,statusErr,phraseErr)
    else:
        httpResponse.setEntityBody(filedata)
    finally:
        responseMessage = httpResponse.getMessage()
        connectionSocket.send(responseMessage.encode('utf-8'))
        connectionSocket.close()



