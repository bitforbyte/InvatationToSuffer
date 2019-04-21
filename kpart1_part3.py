#!/usr/bin/python3
import operator
import string
import sys
import ast

# Batch to hold the values from each batch
class Batch:
    def __init__(self, senders, recievers):
        self.senders = senders                      # Those who sent messages
        self.recievers = recievers                  # Those who recieved messages
    
class User:
    def __init__(self, username):
        self.name = username
        self.numUsers = 260                         # N recipients
        self.numBatch = 32                          # b for batch size

    def setInfo(self, users, batches):
        self.batches = batches
        self.users = users

    def addProb(self, big, recievers):
        for received in recievers:
            # Don't include themselves
            if self.name != received:
                # add the prob of them talking to recipients (1/b)
                if big[received] == 0:
                    big[received] = 1/self.numBatch
                else:
                    big[received] += 1/self.numBatch
        return big
        

    def findFriends(self):
        tPrime = 0      # Number of rounds user hasn't spoken
        bigU = {}       # Final background noise vector

        # Create a dictionary with the users
        for i in self.users:
            bigU[i.name] = 0

        # Number of batches user has spoken
        t = 0

        # Probability of users who recieved message
        bigO = {}   
        for i in self.users:
            bigO[i.name] = 0

        # Find the batch where user doesn't speak
        for batch in self.batches:

            # If the user isn't a sender
            if self.name not in batch.senders:
                tPrime += 1

                # For each user who recieved add 1/b to their background distribution to get SUM(ui) from 1 - t'
                bigU = self.addProb(bigU, batch.recievers)

            else: # When the user Did speak
                t += 1
                bigO = self.addProb(bigO, batch.recievers)

        # Loop through the users and multiply to get the sums
        for users in self.users:
            if tPrime != 0:
                bigU[users.name] *= (1/tPrime)
            
            if t != 0:
                bigO[users.name] *= (1/t)

        # Final Formula to determine most likely 
        vecV = {}
        for i in self.users:
            vecV[i.name] = (1/1) * ((self.numBatch * bigO[i.name]) - (self.numBatch - 1) * bigU[i.name])
        
        # Return list of most likely friends
        return vecV


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
        users.append(User(i[:64]))

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
        batches.append(Batch(sendersList, recieversList))


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