#!/usr/bin/env python3
import sys, re, datetime

class privNode:
    def __init__(self, ident):
        self.id = ident
        self.connected = []

class privateMessages:
    def __init__(self):
        self.messages = {}

    def addMessage(self, seen, message):
        if message not in self.messages:
            self.messages[message] = []

        if seen not in self.messages[message]:
            self.messages[message].append(seen)



def mapPrivate(filename):
    privateNodes = []

    with open(filename) as f:
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

        if curNode != None:
            privateNodes.append(curNode)

    return privateNodes


def netBuster(filename, seek_loc, privateMapping):
    round_done = False
    round_offer_done = False
    round_ack_done = False

    cycle_zero_offer = -1
    cycle_zero_ack = -1

    senders = []
    recievers = []
    next_round_seek = seek_loc

    privOffer = privateMessages()
    privAck = privateMessages()

    with open(filename, 'r') as f:
        f.seek(seek_loc)

        date_time = -1
        while round_done == False:
            cur_seek = f.tell()
            line = f.readline()

            if line == "":
                next_round_seek = -1
                round_done = True
                continue

            timestr = line.split('--')[0]
            timeobj = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
            
            # OFFER part of round
            if "OFFER" in line and round_offer_done == False:

                # First cycle seen
                if cycle_zero_offer == -1:
                    cycle_zero_offer = timeobj.timestamp()
                
                # Skip first cycle
                if abs(timeobj.timestamp() - cycle_zero_offer) <= 3:
                    continue

                # Set second cycle time
                if date_time == -1:
                    date_time = timeobj.timestamp()

                # If this is in cycle 1, 3 second grace period
                if abs(timeobj.timestamp() - date_time) <= 3:
                    node = line.split('--')[1]
                    messages = line.split('--')[2].split('|')

                    for message in messages:
                        message = message.strip()
                        if message.startswith('0'):
                            privOffer.addMessage(node, message)

                # Not in cycle 0
                else:
                    round_offer_done = True
                    date_time = -1

            # Start of ACK sections
            elif "ACK" in line and round_ack_done == False:

                # First cycle of ACK portion
                if cycle_zero_ack == -1:
                    cycle_zero_ack = timeobj.timestamp()

                # Skip first cycle
                if abs(timeobj.timestamp() - cycle_zero_ack) <= 3:
                    continue

                # Set second cycle time
                if date_time == -1:
                    date_time = timeobj.timestamp()

                if abs(timeobj.timestamp() - date_time) <= 3:
                    node = line.split('--')[1]
                    messages = line.split('--')[2].split('|')

                    for message in messages:
                        message = message.strip()
                        if message.startswith('0'):
                            privAck.addMessage(node, message)

                else:
                    round_ack_done = True
                    date_time = -1

            elif round_offer_done == True and round_ack_done == True:
                if "OFFER" in line:
                    next_round_seek = cur_seek
                    round_done = True

            else:
                continue

    for seen in privOffer.messages.values():
        for priv in privateMapping:
            if set(priv.connected) == set(seen):
                senders.append(priv.id)

    for seen in privOffer.messages.values():
        for priv in privateMapping:
            if set(priv.connected) == set(seen):
                recievers.append(priv.id)

    return (next_round_seek, senders, recievers)

def _printUsers(users):
    for i, val, in enumerate(users):
        if i < (len(users) - 1):
            print("'%s', " % val, end='')
        else:
            print("'%s']" % val)


def printRound(senders, recevers):
    print("S:[", end='')
    _printUsers(senders)
    print("R:[", end='')
    _printUsers(recevers)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: part3_a ROUNDS_IN NETWORK_MAP")
        sys.exit(1)

    priv = mapPrivate(sys.argv[2])
    next_seek = 0

    while (next_seek != -1):
        (next_seek, s, r) = netBuster(sys.argv[1], next_seek, priv)
        printRound(s,r)
