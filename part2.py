# Example id VVVV
# 80da3d512c17287e6ec3667d0248ced0e9cf1124a46d49fd5447efd20d7ee440@160.36.57.98:10732

import socket
import sys
import re

# Node in network
class Node:
    def __init__(self, ident):
        self.node_id = ident.split('@')[0]
        self.ip = ident.split('@')[1].split(':')[0]
        self.port = int(ident.split('@')[1].split(':')[1])
        self.public = True
        self.done = False

# Whole network 
class Network:
    def __init__(self):
        self.nodes = {}

    def addNode(self, ident):
        if ident in self.nodes:
            return True
        else:
            self.nodes[ident] = Node(ident)
            return False

# REGEX string to parse PEERS responces
reg = r"^[a-zA-Z0-9]{64}@[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:[0-9]*"
Net = Network()

def launch(IP, PORT):
    sys.stderr.write("Attempting to connect to {} {}\n".format(IP, PORT))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connectCount = 0

    # Attempt to reconnect to server multiple times
    # One may fail for some reason
    while True:
        try:
            s.connect((IP, PORT))
            break
        except:
            if connectCount > 3:
                return False
            else:
                connectCount += 1

    count = 0

    # Catch errors to close connection, 30 min ban bad... ;-;
    try:
        # After 100 tries we probably got all of them
        while count < 100:
            s.send("PEERS\n".encode())
        
            data = bytearray(b'')

            # Grab all responces
            for i in range(0,8):
                data += s.recv(84)

            pdata = data.decode('utf-8')
            bdata = pdata.split('\n')

            # If we got banned exit
            if "BANNED" in pdata:
                print("Banned!");
                print(pdata)
                s.close()
                sys.exit(1);
        
            # for all line in the responce
            for line in bdata:

                # Clear newlines
                if line == "":
                    continue
                
                # If it does not match regex skip it
                if not re.match(reg, line):
                    sys.stderr.write("Line does not look like PEERS responce data\n")
                    sys.stderr.write("\t" + line + "\n")
                    continue

                # Add node, if it has not been added reset cound.
                # Otherwise increment 
                if Net.addNode(line) == False:
                    count = 0
                else:
                    count += 1
        s.close()

        return True

    # Script failed
    except Exception as e:
        print("Script hit error, exiting...")
        print(e)
        s.close()
        sys.exit(1)

if __name__ == "__main__":
    done = False
    launchPoint = "80da3d512c17287e6ec3667d0248ced0e9cf1124a46d49fd5447efd20d7ee440@160.36.57.98:10732"
    launchPointIP = "160.36.57.98"
    launchPointPort = 10732

    # Add initial node
    Net.addNode(launchPoint)

    while done == False:
        done = True

        # Cannot modify dict while iterating through so make a copy
        for k,v in Net.nodes.copy().items():

            sys.stderr.write("Looking at node {}@{}:{}\n".format(v.node_id, v.ip, v.port))

            if v.done == False:
                done = False
                Net.nodes[k].public = launch(v.ip, v.port)
                Net.nodes[k].done = True

    if len(sys.argv) > 1 and sys.argv[1] == 'y':
        for v in Net.nodes.copy().values():
            if v.public == True:
                print("{},{},{}".format(v.node_id, v.ip, v.port))
    else:
        for v in Net.nodes.copy().values():
            print("{}@{}:{}".format(v.node_id, v.ip, v.port))
