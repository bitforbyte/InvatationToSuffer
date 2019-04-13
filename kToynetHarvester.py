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

def findPeers(nodeID, tcp_port, soc):
    nodes = []
    counter = 0

    # Send PEERS commands until 
    while(counter < 100):
        
        soc.send("PEERS\n".encode('utf-8'))
        data = soc.recv(BUFFER_SIZE)
        
        parsedata = data.decode('utf-8')

        # Check to see if Punished
        if parsedata.find('BANNED') != -1:
            num = re.search("\d+\.\d+", parsedata)
            print("BANNED: Flail thy self for %s minutes" % num.group(0))
            raise ConnectionResetError()

        dataBreak = parsedata.split('\n')

        # Loop through the split data
        for each in dataBreak:

            # If it's a string
            if each:
                # Attempt to read the PEER data
                try:
                    # Regex commands to find info
                    nIDSearch = re.search('8(.*)@', each)
                    #ipAddrSearch = re.search('@(.*):', each)
                    nodePortSearch = re.search(':(.*)', each)
                    
                    if nIDSearch and nodePortSearch:
                        # re returns structure group(0) is the value found
                        nID = nIDSearch.group(0)[:-1]
                        nodePort = nodePortSearch.group(0)[1:]

                        if len(nID) == 64:
                            # Test if the peer exists
                            test = 0
                            for i in nodes:
                                if i.id == nID:
                                    test = 1
                                    break

                            if test == 1: 
                                counter += 1
                            else:
                                # Add the nodes
                                nodes.append(Node(nID, nodePort))

                                # Reset the counter if one is found
                                counter = 0 
                    break
                except AttributeError:
                    print("Error:")
                   
    return nodes


if __name__== "__main__":
    # Default from bootstrap
    tcp_port = 10732

    connections = []
    

    users = []

    # Entry point
    users.append(Node('80da3d512c17287e6ec3667d0248ced0e9cf1124a46d49fd5447efd20d7ee440', tcp_port))

    # Keep track of users we've been to
    contacted = [users[0]]

    # For loop
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.connect((TCP_IP, tcp_port))
    connections.append(soc)
    try:
        peers = findPeers(users[0].id,users[0].port, connections[0])
        print('peers: ')

        for i in peers:
            print(i.id, ' ',end='')
            print(i.port)
        users.extend(peers)
    except KeyboardInterrupt:
        print("Closing")
    except ConnectionResetError as error:
        print("Connection reset by peer")
        #print(re.search('b\'*\n', error))
    except NameError:
        print("Name Error")

    # For Loop closing
    connections[0].close()