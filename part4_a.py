#!/usr/bin/env python3
import sys

class privNode:
    def __init__(self, id):
        self.id = id
        self.connected = []

privateNodes = []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    with open(sys.argv[1]) as f:
        lines = f.readlines()

        curNode = None

        for line in lines:
            line = line.strip()
            
            if line.startswith(">") == False:
                if curNode != None:
                    privateNodes.append(curNode)

                t = line.split(',')[1].replace(":", "")
                if t == "False":
                    curNode = privNode(line.split('@')[0])
                else:
                    curNode = None

            else:
                if curNode != None:
                    curNode.connected.append(line.split('@')[0].replace('>',''))

        for priv in privateNodes:
            print("{} : {}".format(priv.id, len(priv.connected)))
            '''
            print("{}".format(priv.id), end='')
            for i in priv.connected:
                print(", {}".format(i), end='')
            print("")
        '''
