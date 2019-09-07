#!/usr/bin/env python3
import os, binascii, random, sys

# Generate users for the mix network
def genUsers(nameLen, numUsers):
    users = []
    for i in range(numUsers):
        # Generate unique users
        while True:
            user = ''.join([str(y) for x in range(nameLen) for y in random.choice('0123456789abcdef')])
            if user not in users:
                break
        users.append(user)
    return users

class MixGen:
    def __init__(self, nameLen, numUsers, numFriends, batchSize, rounds,seed=random.seed()):
        self.nameLen = nameLen
        self.numUsers = numUsers
        self.numFriends = numFriends
        self.batchSize = batchSize
        self.numRounds = rounds
        self.users = genUsers(self.nameLen,self.numUsers)
        random.seed(seed)
        
    # Generate the friends for the user to talk to, default is 2 friends per user
    def genFriends(self):
        friendDict = {}

        for user in self.users:
            # Generate friends for user
            # NOTE May need to use Power distribution to select friends
            friends = random.choices(self.users, k=self.numFriends)

            # User shouln't be there own friend, no duplicates
            while(user in friends or len(friends) != len(set(friends))):
                friends = random.choices(self.users, k=self.numFriends)
            friendDict[user] = friends

        return friendDict
    
    # Generate the messages sent between users and their friends
    # Will create list (size: numRounds*2) of senders and recievers
    # Users will be selected randomly by batchsize to communicate
    def genRound(self, friendDict):
        users = list(friendDict.keys())

        # Pick batchsize random users
        senders = random.choices(users, k=self.batchSize)
        recievers = []
        for user in senders:
            choice = random.randrange(0,self.numFriends)
            recievers.append(friendDict[user][choice])
        
        # Shuffle the senders and recivers
        random.shuffle(senders)
        random.shuffle(recievers)

        # Convert to string
        sendersStr = "S:['" + "','".join(senders) + "']\n"
        recieversStr = "R:['" + "','".join(recievers) + "']\n" 
        return sendersStr, recieversStr

    # Write the file to check if
    def writetoFile(self, users, friends, rounds):
        wf = open("_UsersGen.txt", "w")
        for user in users:
            wf.write(user+'\n')
        wf.close()

        wf = open("_FriendsGen.txt", "w")
        for user in friends:
            outData = "%s: %s,%s\n" %(user, friends[user][0], friends[user][1])
            wf.write(outData)
        wf.close()
            
        wf = open("_RoundsGen.txt", "w")
        for i in range(0,len(rounds), 2):
            wf.write(rounds[i])
            wf.write(rounds[i+1])
        wf.close()

    # Create the rounds (users, friends, and rounds)
    def createRounds(self, write=False):
        # TODO add length error check
        friendDict = self.genFriends()
        rounds = []

        for i in range(self.numRounds):
            senders, recievers = self.genRound(friendDict)
            rounds.append(senders)
            rounds.append(recievers)

        if (write):
            self.writetoFile(self.users, friendDict, rounds)
        
        return self.users, friendDict, rounds