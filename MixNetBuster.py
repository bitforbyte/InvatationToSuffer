#!/usr/bin/python3
import operator
import string
import sys
import ast

class NetBuster:
    def __init__(self, users, rounds, numBatch):
        self.numUsers = len(users)
        self.numBatch = numBatch
        self.rounds = rounds
        self.users = users

    def addProb(self, name, big, recievers):
        for received in recievers:
            # Don't include themselves
            if name != received:
                # add the prob of them talking to recipients (1/b)
                if big[received] == 0:
                    big[received] = 1/self.numBatch
                else:
                    big[received] += 1/self.numBatch
        return big
        
    # Will deanonymize using a statistical analysis attack
    def deanonymize(self, currUser):
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
        for batch in self.rounds:

            # If the user isn't a sender
            if currUser not in batch.senders:
                tPrime += 1

                # For each user who recieved add 1/b to their background distribution to get SUM(ui) from 1 - t'
                bigU = self.addProb(currUser, bigU, batch.recievers)

            else: # When the user Did speak
                t += 1
                bigO = self.addProb(currUser, bigO, batch.recievers)

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

# Batch to hold the values from each batch
class Round:
    def __init__(self, senders, recievers):
        self.senders = senders                      # Those who sent messages
        self.recievers = recievers                  # Those who recieved messages
    
class User:
    def __init__(self, username):
        self.name = username