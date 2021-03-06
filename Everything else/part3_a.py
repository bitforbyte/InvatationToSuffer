#!/usr/bin/env python3
import sys, re, datetime

def net_buster(filename, seek_loc):
    round_done = False
    round_offer_done = False
    round_ack_done = False

    senders = []
    recievers = []
    next_round_seek = seek_loc

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
                if date_time == -1:
                    date_time = timeobj.timestamp()

                # If this is in cycle 0, 3 second grace period
                if abs(timeobj.timestamp() - date_time) <= 3:
                    node = line.split('--')[1]
                    messages = line.split('--')[2].split('|')

                    for message in messages:
                        message = message.strip()
                        if message == "OFFER" or message == "":
                            continue
                        else:
                            senders.append(node)

                # Not in cycle 0
                else:
                    round_offer_done = True
                    date_time = -1

            # 
            elif "ACK" in line and round_ack_done == False:
                if date_time == -1:
                    date_time = timeobj.timestamp()

                if abs(timeobj.timestamp() - date_time) <= 3:
                    node = line.split('--')[1]
                    messages = line.split('--')[2].split('|')

                    for message in messages:
                        message = message.strip()
                        if message == "ACK" or message == "":
                            continue
                        else:
                            recievers.append(node)

                else:
                    round_ack_done = True
                    date_time = -1

            elif round_offer_done == True and round_ack_done == True:
                if "OFFER" in line:
                    next_round_seek = cur_seek
                    round_done = True

            else:
                continue

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
    if len(sys.argv) < 2:
        sys.exit(1)
    
    next_seek = 0

    while (next_seek != -1):
        (next_seek, s, r) = net_buster(sys.argv[1], next_seek)
        printRound(s,r)
