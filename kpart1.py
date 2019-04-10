#!/usr/bin/python3
import operator
import string
import sys
import ast

# Batch to hold the values from each batch
class Batch:
	def __init__(self, senders, recievers):
		self.senders = senders						# Those who sent messages
		self.recievers = recievers					# Those who recieved messages
	
class User:
	def __init__(self, username):
		self.name = username
		self.numUsers = 260				# N recipients
		self.numBatch = 32				# b for batch size

	def setInfo(self, users, batches):
		self.batches = batches
		self.users = users

	def findFriends(self):
		# Find u
		tPrime = 0
		bigU = {}
		for i in self.users:
			bigU[i.name] = 0

		# Find the batch where user doesn't speak
		for batch in self.batches:
			# If the user isn't a sender
			if self.name not in batch.senders:
				tPrime += 1

				# For each user who recieved add 1/b to their background distribution to get SUM(ui) from 1 - t'
				for received in batch.recievers:
					if self.name != received:
						if bigU[received] == 0:
							bigU[received] = 1/self.numBatch
						else:
							bigU[received] += 1/self.numBatch
		
		# Multiply 1/t' to each of the users resulting in Ubar
		for users in bigU:				
			bigU[users] *= (1/tPrime)

		t = 0
		bigO = {}
		for i in self.users:
			bigO[i.name] = 0

		# Loop through the batches
		for batch in self.batches:
			# See if the name is in the senders
			if self.name in batch.senders:
				t += 1

				for received in batch.recievers:
					if self.name != received:
						if bigO[received] == 0:
							bigO[received] = 1/self.numBatch
						else:
							bigO[received] += 1/self.numBatch

		for users in bigO:
			bigO[users] += (1/t)
		

		vecV = {}
		for i in self.users:
			vecV[i.name] = (1/1) * ((self.numBatch * bigO[i.name]) - (self.numBatch - 1) * bigU[i.name])

		return vecV
		# Return list of most likely friends

if __name__== "__main__":

	users = []
	for i in range(0, 26):
		letter = dict(zip(range(0, 26), string.ascii_lowercase))	
		for j in range(0, 10):
			letterName = letter[i] + string.digits[j]	# Get the letter names (a-z)(0-9)
			users.append(User(letterName))				# Users list that will hold each of the users in a class		

	# Read in the batches into a list
	# List to hold each batch
	batches = []

	#lines = sys.stdin.readlines()	# Holds the raw input text
	file = open("dataset.raw", "r")
	lines = file.readlines()
	file.close()
	#numBatch = 0	# number of batches used for index (used for debug printing)
	
	# Loop through lines by 2 for S and R pairs
	for i in range(0, len(lines)-1,2):

		# Trim the sender and reciever lists to obtain a list of names
		sendersList = ast.literal_eval(lines[i][2:])		
		recieversList = ast.literal_eval(lines[i+1][2:])

		# assign the Senders and Recievers into the batch list
		batches.append(Batch(sendersList, recieversList))


	users[0].setInfo(users, batches)
	final = users[0].findFriends()

	sorted_final = sorted(final.items(), key=lambda kv: kv[1])
	print (sorted_final)
	#for user in users:
	#	user.setInfo(users, batches)
	#	user.findFriends()
		#print(user.findFriends())