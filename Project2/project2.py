import pandas as pd
import time
from numpy.random import randint as rnd
import operator

def sarsaLambda(l,data):
	#Sarsa Lambda algorithm for estimating Bellman Equation

	#Initialize lambda, alpha and gamma (arbitrary for now)
	alpha = 0.1		#alpha
	gamma = 0.5		#gamma

	#Initialize Q (Expected Rewards) and N ([s,a] visit counts) dictionaries
	Q = {}
	N = {}

	#Loop through each row in the data
	for t in range(data.shape[0]):

		if t == 0:
			s = data.s[t]		#get state
			a = data.a[t]		#get action
			r = data.r[t] 		#get reward
			sp = data.sp[t] 	#get next state
			N.clear()
			continue

		sKey = str(s) + ',' + str(a)
		spKey = str(sp) + ',' + str(data.a[t])

		if sKey in N:
			N[sKey] += 1 		#increment counts
		else:
			N[sKey] = 1

		if sKey not in Q:
			Q[sKey] = 0
		
		if spKey not in Q:
			Q[spKey] = 0

		delta = r + gamma*Q[spKey] - Q[sKey] #calculate delta

		#Smear reward through state-action space
		#	If s-a pair has no counts, update would be 0
		for idx in N:
			Q[idx] += alpha*delta*N[idx]
			N[idx] = gamma*l*N[idx]

		if data.s[t] != sp:
			N.clear()

		s = data.s[t]		#get state
		a = data.a[t]		#get action
		r = data.r[t] 		#get reward
		sp = data.sp[t] 	#get next state

	return(Q)

def extractPolicy(filename,nS,nA,learnedQ):
    with open(filename, 'w') as f:
        for state in range(nS):

        	stateQs = {key:val for key,val in learnedQ.items() if str(state+1)+',' in key}

        	if not stateQs:
        		a = rnd(1,nA)
        	else:
        		maxKey = max(stateQs.items(), key=operator.itemgetter(1))[0]
        		a = int(maxKey.split(',')[-1])

        	f.write("{}\n".format(a))

def compute(inFile,outFile):
	csvData = pd.read_csv(inFile)                      #read in data from .csv file

	if inFile == "small.csv":
		l = 0.95
		numStates = 100
		numActions = 4
	elif inFile == "medium.csv":
		l = 1
		numStates = 50000
		numActions = 7
	elif inFile == "large.csv":
		l = 0.95
		numStates = 312020
		numActions = 9
	else:
		print("Input Filename Error")
		return()

	time.clock()
	learnedQ = sarsaLambda(l,csvData)
	print(time.clock())

	extractPolicy(outFile,numStates,numActions,learnedQ)

	print(time.clock())
	
	pass

def main():
    if len(inputs) != 2:
        raise Exception("usage: <infile>.csv <outfile>.gph")

    inputfilename = inputs[0]
    outputfilename = inputs[1]
    compute(inputfilename, outputfilename)

if __name__ == '__main__':
    inputs = ["large.csv","large.policy"]
    main()