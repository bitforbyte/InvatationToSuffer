#!/usr/bin/env python3
import sys, operator

class Node:
    def __init__(self, name):
        self.name = name;
        self.peopleDict = {}
    def addReceiver(self, rname):
        if rname == self.name:
            return

        if rname in self.peopleDict:
            self.peopleDict[rname] += 1
        else:
            self.peopleDict[rname] = 1

    def probableFriends(self):
        return sorted(self.peopleDict.items(), key=operator.itemgetter(1), reverse=True)[:3]

if __name__ == "__main__":
    lines = sys.stdin.readlines()

    Nodes = {}

    for i in range(0, 26):
        for j in range(0, 10):
            name = chr(i+97) + str(j)
            Nodes[name] = Node(name)


    for i in range(0, len(lines), 2):
        if not lines[i].strip():
            break

        senders = lines[i].strip("S[:]\n").replace("'","").replace(" ", "").split(',')
        receivers = lines[i+1].strip("R[:]\n").replace("'","").replace(" ", "").split(',')

        for send in senders:
            for rec in receivers:
                Nodes[send].addReceiver(rec)

    i = 0
    for k,node in Nodes.items():
        friends = node.probableFriends()
        print("%s,%s,%s,%s" % (node.name, friends[0][0], friends[1][0], friends[2][0]))
