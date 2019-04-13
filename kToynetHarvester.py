#!/usr/bin/python3
import time
import socket
import re

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
    
    #soc.settimeout(10)
    
    ids = []
    count = 0
    while(count < 30):
        soc.send("PEERS\n".encode('utf-8'))
        data = soc.recv(BUFFER_SIZE)
        parsedata = data.decode('utf-8')
        dataBreak = parsedata.split('\n')
        #print(dataBreak)

        for each in dataBreak:
            print(' ' + each,end='')
            if each:
                nodeId = re.search('8(.*)@', each)
                ipAddr = re.search('@(.*):', each)
                nodePort = re.search(':(.*)\n', each)
                print('%s %s %s\n' % (nodeId.group(1), ipAddr.group(1), nodePort.group(1)))
            else:
                print(' - Not String')
            #if each and not each.isspace():
            #nodeId = re.search('8(.*)@', each)
            #ipAddr = re.search('@(.*):', each)
            #nodePort = re.search(':(.*)\n', each)
            #print('%s %s %s\n' % (nodeId.group(1), ipAddr.group(1), nodePort.group(1)))
        count += 1

    soc.close() 

