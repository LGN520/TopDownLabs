#!/usr/bin/env python
from socket import *
import threading
import signal

# only support GET method now

class ConstantVar(object):
    # Http format info
    sp = ' '
    crlf = '\r\n'
    colon = ':'

    # response line
    version = 'HTTP/1.1'
    statusOK = '200'
    statusErrInvalidMethod = '405'
    phraseOK = 'OK'
    phraseErrInvalidMethod = 'Not Allowed Method'

    # header line
    contentTypeName = 'Content-Type'
    contentTypeValue = 'test/html'

    # Proxy server info
    proxyPort = 8000
    serverPort = 80
    maxLength = 1024

    # available methods
    availableMethods = ['GET']

    # timeout
    timeout = 5

    @staticmethod
    def buildHeaderLine(name, value):
        return name + ConstantVar.colon + ConstantVar.sp + value + ConstantVar.crlf

class HttpRequest(object):
    def __init__(self, requestMessage):
        # request message includes request line, header lines, blank line, entity body
        length = len(requestMessage)
        blankLineIndex = requestMessage.find(ConstantVar.crlf*2)+2

        # request body
        bodyIndex = blankLineIndex + 2
        if bodyIndex >= length:
            self.__body = ""
        else:
            self.__body = requestMessage[bodyIndex:]

        # request header(request line + header lines)
        self.__head = requestMessage[0:blankLineIndex-2]
        self.__lines = self.__head.split(sep=ConstantVar.crlf)

        self.__headerLines = {}
        for i in range(len(self.__lines)):
            if i == 0:
                tempFields = self.__lines[i].split(sep=ConstantVar.sp)
                # request line(method + url + version)
                self.__requestLineMethod = tempFields[0]
                self.__requestLineUrl = tempFields[1]
                self.__requestLineVersion = tempFields[2]
            else:
                spIndex = self.__lines[i].find(ConstantVar.sp)
                # key: value
                key = self.__lines[i][0:spIndex-1]
                value = self.__lines[i][spIndex+1:]
                self.__headerLines[key] = value

    def getMethod(self):
        return self.__requestLineMethod

    def getUrl(self):
        return self.__requestLineUrl

    def getVersion(self):
        return self.__requestLineVersion

    def getValue(self, key):
        return self.__headerLines[key]

class HttpResponse(object):
    def __init__(self):
        # fields of status line
        self.__version = ConstantVar.version
        self.__status = ConstantVar.statusOK
        self.__phrase = ConstantVar.phraseOK

        # fileds of header lines
        self.__contentTypeName = ConstantVar.contentTypeName
        self.__contentTypeValue = ConstantVar.contentTypeValue

        # entity body
        self.__entityBody = ''

    def setStatusLine(self, version, status, phrase):
        self.__version = version
        self.__status = status
        self.__phrase = phrase

    def setEntityBody(self, data):
        self.__entityBody = data

    def getMessage(self):
        statusLine = self.__version + ConstantVar.sp + self.__status + ConstantVar.sp + self.__phrase + ConstantVar.crlf

        contentTypeLine = ConstantVar.buildHeaderLine(self.__contentTypeName, self.__contentTypeValue)
        headerLines = contentTypeLine

        blankLine = ConstantVar.crlf

        return statusLine + headerLines + blankLine + self.__entityBody

class WebProxy(object):
    def __init__(self, port):
        self.__port = port
        self.__socket = socket(AF_INET, SOCK_STREAM)

    def __proxyFunc(connSocket, connAddr):
        try:
            recvMessageBytes = connSocket.recv(ConstantVar.maxLength)

            recvMessage = recvMessageBytes.decode('utf-8')
            print(recvMessage)
            httpRequest = HttpRequest(recvMessage)
            method = httpRequest.getMethod()

            if method in ConstantVar.availableMethods:
                hostname = httpRequest.getValue("Host")
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((hostname, ConstantVar.serverPort))
                clientSocket.send(recvMessageBytes)
                responseMessageBytes = clientSocket.recv(ConstantVar.maxLength)
                print(responseMessageBytes)
                clientSocket.close()
                connSocket.send(responseMessageBytes)
            else:
                httpResponse = HttpResponse()
                httpResponse.setStatusLine(ConstantVar.version,ConstantVar.statusErrInvalidMethod,ConstantVar.phraseErrInvalidMethod)
                connSocket.send(httpResponse.getMessage().encode('utf-8'))
        except Exception as e:
            print(e)
        finally:
            connSocket.close()
            exit(0)

    def start(self):
        self.__socket.bind(('', self.__port))
        self.__socket.listen(1)
        while True:
            connSocket, connAddr = self.__socket.accept()
            t = threading.Thread(target=WebProxy.__proxyFunc, args=(connSocket, connAddr))
            t.start()

    def end(self):
        self.__socket.close()

def main():
    webProxy = WebProxy(ConstantVar.proxyPort)
    webProxy.start()

if __name__ == '__main__':
    main()