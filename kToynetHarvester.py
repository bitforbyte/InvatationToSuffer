#!/usr/bin/env python

import socket

TCP_IP = '160.36.57.98'
TCP_PORT = 10722
BUFFER_SIZE = 1024
MESSAGE = "PEERS"

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((TCP_IP, TCP_PORT))
soc.send(MESSAGE)
data = soc.recv(BUFFER_SIZE)
soc.close() 
