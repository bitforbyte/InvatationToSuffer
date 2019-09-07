#!/usr/bin/python3
import operator
import string
import sys
import ast
import NetBuster

def main():
    #users = []
    fileName = open("_UsersGen.txt", "r") # TODO Replace file input for stdin
    userNames = fileName.readlines()
    fileName.close()
    users = []
    for user in userNames:
        users.append(NetBuster.User(user.rstrip()))    # Users list that will hold each of the users in a class  
    # Read in the batches into a list
    # List to hold each batch
    rounds = []

    fileName = open("_RoundsGen.txt", "r") # TODO Replace file input for stdin
    lines = fileName.readlines()
    fileName.close()  

    # Loop through lines by 2 for S and R pairs
    for i in range(0, len(lines)-1,2):

        # Trim the sender and reciever lists to obtain a list of names
        sendersList = ast.literal_eval(lines[i][2:])        
        recieversList = ast.literal_eval(lines[i+1][2:])

        # assign the Senders and Recievers into the batch list
        rounds.append(NetBuster.Round(sendersList, recieversList))


    for i in range(0, 260):
        users[i].setInfo(users, rounds)
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

if __name__== "__main__":
    main()
    