#!/usr/bin/python3
import operator
import string
import sys
import ast
import NetBuster

if __name__== "__main__":

    # Read in the batches into a list
    # List to hold each batch
    batches = []

    #TODO add users to file from part 2 (pub and priv)
    users = []
    file = open("peers.txt", "r")
    lin = file.readlines()
    file.close()

    for i in lin:
        #print(i[:64])
        users.append(NetBuster.User(i[:64]))

    lines = sys.stdin.readlines()

    #Sam's return function call (loop? that covers everything below)
    # return function gives New start spot, senders array, receivers array
    # StartLoc, sendersList, recieversList = funcReturn()
    

    # Loop through lines by 2 for S and R pairs
    for i in range(0, len(lines)-1,2):

        # Trim the sender and reciever lists to obtain a list of names
        # set senderslist/recievers list above in tuple
        sendersList = ast.literal_eval(lines[i][2:])        
        recieversList = ast.literal_eval(lines[i+1][2:])

        # assign the Senders and Recievers into the batch list
        batches.append(NetBuster.Round(sendersList, recieversList))


    for i in range(0, len(users)):
        #print(i)
        #users might need to be changed to IDlist
        users[i].setInfo(users, batches)
        final = users[i].findFriends()
        print(users[i].name, end='')

        # Sort in Decending order
        sorted_final = sorted(final.items(), key=lambda kv: kv[1], reverse=True)
        count = 0

        # Print the first 3 friends
        for key in sorted_final:
            print(',' + key[0], end='')
            count += 1
            if count == 3:
                    print()
                    break