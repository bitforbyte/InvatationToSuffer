import os, binascii, random, sys
from datetime import datetime
class MixGen:
    def __init__(self, nameLen, numUsers, numFriends, batchSize, seed=random.seed()):
        self.nameLen = nameLen
        self.numUsers = numUsers
        self.numFriends = numFriends
        self.batchSize = batchSize
        random.seed(seed)

    # Generate users
    def genUsers(self):

        users = []
        for i in range(self.numUsers):
            # Generate unique users
            while True:
                user = ''.join([str(y) for x in range(self.nameLen) for y in random.choice('0123456789abcdef')])
                if user not in users:
                    break
            
            
            users.append(user)
        return users

    def genFriends(self, users):
        friendDict = {}

        for user in users:
            # Generate friends for user
            # NOTE May need to use Power distribution to select friends
            friends = random.choices(users, k=self.numFriends)

            # User shouln't be there own friend, no duplicates
            while(user in friends or len(friends) != len(set(friends))):
                friends = random.choices(users, k=self.numFriends)
            friendDict[user] = friends

        return friendDict
    
    def genRound(self, friendDict):
        users = list(friendDict.keys())

        # Pick batchsize random users
        senders = random.choices(users, k=self.batchSize)
        recievers = []
        for user in senders:
            choice = random.randrange(0,self.numFriends)
            recievers.append(friendDict[user][choice])
        random.shuffle(senders)
        random.shuffle(recievers)
        sendersStr = "S:['" + "','".join(senders) + "']\n"
        recieversStr = "R:['" + "','".join(recievers) + "']\n" 
        return sendersStr, recieversStr

def main(argv):
    mg = MixGen(4, 260, 2, 32)
    numRounds = 250
    # TODO add length error check
    users = mg.genUsers()

    wf = open("_UsersGen.txt", "w")
    for user in users:
        wf.write(user+'\n')
    wf.close()

    friendDict = mg.genFriends(users)

    wf = open("_FriendsGen.txt", "w")
    for user in friendDict:
        outData = "%s: %s,%s\n" %(user, friendDict[user][0], friendDict[user][1])
        wf.write(outData)
    wf.close()
        
    wf = open("_RoundsGen.txt", "w")
    for i in range(numRounds):
        senders, recievers = mg.genRound(friendDict)
        wf.write(senders)
        wf.write(recievers)
    wf.close()
    

if __name__ == "__main__":
    main(sys.argv[1:])