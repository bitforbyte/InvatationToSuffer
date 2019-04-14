#!/usr/bin/python3
import time
import socket
import re
import operator

TCP_IP = '160.36.57.98'
BUFFER_SIZE = 1024

class Network:
    def __init__(self):
        self.nodes = []
    
    # Add user to the network
    def addUser(self, node):
        exists = 0
        for i in self.nodes:
            if i.id == node.id:
                exists = 1
                break
        # If it isn't in the nodes add it
        if exists == 0:
            self.nodes.append(node)

    # Write the users to the given file
    def writeNetwork(self, fil):
        fileName = open(fil, 'w')
        self.nodes.sort(key=lambda x:str(x.port))
        for node in self.nodes:
            fileName.write(node.id + "@" + TCP_IP + ":" + str(node.port) + "\n")
        fileName.close()

    def findPeers(self, nodeID, soc):
        counter = 0

        # Send PEERS commands until 
        while(counter < 100):
            
            soc.send("PEERS\n".encode('utf-8'))
            data = soc.recv(BUFFER_SIZE)
            
            parsedata = data.decode('utf-8')

            # Check to see if Punished
            if parsedata.find('BANNED') != -1:
                num = re.search("\d+\.\d+", parsedata)
                print("BANNED: Flail thyself for %s minutes" % num.group(0))
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
                        
                        # Make sure they searches exists
                        if nIDSearch and nodePortSearch:
                            # re returns structure group(0) is the value found
                            nID = nIDSearch.group(0)[:-1]
                            nodePort = nodePortSearch.group(0)[1:]

                            # Make sure the id is 64 characters long
                            if len(nID) == 64:
                                # Test if the peer exists
                                test = 0
                                for i in self.nodes:
                                    if i.id == nID:
                                        test = 1
                                        break

                                if test == 1: 
                                    counter += 1
                                else:
                                    # Add the nodes
                                    self.nodes.append(Node(nID, nodePort))

                                    # Reset the counter if one is found
                                    counter = 0 
                    except AttributeError:
                        print("Error:")       
        return self.nodes

class Node:
    def __init__(self, nodeId, port):
        self.id = nodeId
        self.port = port

if __name__== "__main__":
    # Default from bootstrap
    tcp_port = 10732

    connections = []
    net = Network()

    # Entry point
    net.nodes.append(Node('80da3d512c17287e6ec3667d0248ced0e9cf1124a46d49fd5447efd20d7ee440', tcp_port))
   
    # Keep track of users we've been to
    contacted = []

    # For loop
    for user in net.nodes:
        print(user.id)
        if user.id not in contacted:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                soc.connect((TCP_IP, int(user.port)))
            except ConnectionRefusedError:
                net.addUser(user)
                continue
            connections.append(soc)

            # try to catch any errors and close connection
            try:
                peers = net.findPeers(user.id, soc)                  

                for peer in peers:
                    net.addUser(peer)
                    
                contacted.append(user.id)
            except KeyboardInterrupt:
                print("\nClosing")
            except ConnectionResetError as error:
                print("Connection reset by peer")
                #print(re.search('b\'*\n', error))
            except NameError:
                print("Name Error")

    net.writeNetwork("peers.txt")

    # For Loop closing
    for con in connections:
        con.close()