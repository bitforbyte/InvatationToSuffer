#!/usr/bin/python3

import socket

TCP_IP = '160.36.57.98'
BUFFER_SIZE = 1024

class Node:
    def __init__(self, nodeId, port):
        self.id = nodeId
        self.port = port

if __name__== "__main__":

    # Default from bootstrap
    tcp_port = 10732

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((TCP_IP, tcp_port))
    nodes = []
    nodes.append(Node('80da3d512c17287e6ec3667d0248ced0e9cf1124a46d49fd5447efd20d7ee440', tcp_port))
    
    #while(1):
    soc.send("PEER\n")
    
    while(1):
        data = soc.recv(BUFFER_SIZE)

    print('received:' + repr(data))
    soc.close() 
