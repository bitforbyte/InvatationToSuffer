#!/usr/bin/env python3
import sys, operator

class Node:
    def __init__(self, name):
        self.name = name;
        self.sent = 0
        self.notSent = 0
        self.peopleDict = {}
        self.notPeopleDict = {}
    def addReceiver(self, rname):
        if rname == self.name:
            return

        self.sent += 1

        if rname in self.peopleDict:
            self.peopleDict[rname] += 1
        else:
            self.peopleDict[rname] = 1

    def addNotSender(self, rname):
        if rname == self.name:
            return

        self.notSent += 1

        if rname in self.notPeopleDict:
            self.notPeopleDict[rname] += 1
        else:
            self.notPeopleDict[rname] = 1
        

    def probableFriends(self):
        probDict = {}
        for k,v in self.peopleDict.items():
            if k not in self.notPeopleDict:
                notVal = 0
            else:
                notVal = self.notPeopleDict[k]
            probDict[k] = abs((v/self.sent) - (notVal / self.notSent))
        return sorted(probDict.items(), key=operator.itemgetter(1), reverse=True)[:3]

if __name__ == "__main__":
    lines = sys.stdin.readlines()

    Nodes = {}

    for j in range(0, 26):
        for i in range(0, 10):
            name = chr(i+97) + str(j)
            Nodes[name] = Node(name)


    for i in range(0, len(lines), 2):
        if not lines[i].strip():
            break

        senders = lines[i].strip("S[:]\n").replace("'","").replace(" ", "").split(',')
        receivers = lines[i+1].strip("R[:]\n").replace("'","").replace(" ", "").split(',')

        for k,v in Nodes.items():
            if v.name in senders:
                for rec in receivers:
                    v.addReceiver(rec)
            else:
                for rec in receivers:
                    v.addNotSender(rec)

    for k,node in Nodes.items():
        friends = node.probableFriends()
        print("%s,%s,%s,%s" % (node.name, friends[0][0], friends[1][0], friends[2][0]))
