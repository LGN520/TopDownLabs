#!/usr/bin/env python

# actually we should implement ICMP protocol, but here we just implement UDP pinger for simplicity
import time
import random
from socket import *

# Pinger info
pingCount = 10
waitTime = 1
message = 'data'

# Server info
serverIP = 'localhost'
serverPort = 9601
maxLength = 1024
serverAddress = (serverIP, serverPort)

clientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
clientSocket.settimeout(waitTime)

count = 0
while(count<pingCount):
    clientSocket.sendto(message, serverAddress)
    try:
        start_time = time.clock()
        recvMessage, _ = clientSocket.recvfrom(maxLength)
        RTT = time.clock()-start_time
        print("RTT of Ping {:d}: {:f}".format(count,RTT))
    except:
        print("Loss of Ping {:d}".format(count))
    finally:
        count = count + 1
clientSocket.close()