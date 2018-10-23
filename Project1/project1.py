import networkx as nx

import pandas as pd

from scipy.special import gammaln

from functools import reduce

import matplotlib.pyplot as plt

from numpy.random import randint as rnd

from numpy.random import shuffle

import time

def write_gph(dag, idx2names, filename):
    with open(filename, 'w') as f:
        for edge in dag.edges():
            f.write("{}, {}\n".format(idx2names[edge[0]], idx2names[edge[1]]))

def bayesianNodeScore(node,data,scoreDag,idxNames):
	#Calculates contribution to Bayesian Score from node
	r = data.max()[node] #R_i for node

	score = 0

	parents = list(scoreDag.pred[node])

	nodeGroup = [node]+parents
	compressedData = pd.DataFrame({'count' : data.groupby([x for x in idxNames[nodeGroup]]).size()}).reset_index()

	for state in compressedData.values:
		score += gammaln(1+state[-1]) - gammaln(1)

	if parents:
		compData0 = pd.DataFrame({'count' : data.groupby([x for x in idxNames[parents]]).size()}).reset_index()
		for data0 in compData0.values:
			score += gammaln(r) - gammaln(r+data0[-1])
	else:
		score += gammaln(r) - gammaln(r+compressedData['count'].sum())

	return(score)

def greedyLocal(data,dag,idx2names):

	score = 0
	for i in range(len(idx2names)):
		score += bayesianNodeScore(i,data,dag,idx2names)     #Calculate Bayesian score of DAG

	print(score)

	currentScore = score
	score -= 1
	loopCount = 0

	while currentScore > score and loopCount < 100:

		score = currentScore
		nodes = list(range(len(idx2names)))
		shuffle(nodes)
		parents = list(range(len(idx2names)))
		shuffle(parents)

		for node in nodes:

			for parent in [x for x in parents if x != node]:

				tempDag = dag.copy()
				bareScore = currentScore - bayesianNodeScore(node,data,tempDag,idx2names)

				reverseScore = 0
				removeScore = 0
				addScore = 0

				if parent in list(tempDag.pred[node]):
					tempDag.remove_edge(parent,node)
					if not list(nx.simple_cycles(tempDag)):
						removeScore = bareScore + bayesianNodeScore(node,data,tempDag,idx2names)

					tempDag.add_edge(node,parent)
					if not list(nx.simple_cycles(tempDag)):
						reverseScore = removeScore - bayesianNodeScore(parent,data,dag,idx2names) + bayesianNodeScore(parent,data,tempDag,idx2names)

					if removeScore > reverseScore and removeScore > currentScore and removeScore != 0:
						dag.remove_edge(parent,node)
						currentScore = removeScore
					elif reverseScore > removeScore and reverseScore > currentScore and reverseScore != 0:
						dag.remove_edge(parent,node)
						dag.add_edge(node,parent)
						currentScore = reverseScore

				elif node not in list(tempDag.pred[parent]):
					tempDag.add_edge(parent,node)
					if not list(nx.simple_cycles(tempDag)):
						addScore = bareScore + bayesianNodeScore(node,data,tempDag,idx2names)

					if addScore > currentScore and addScore != 0:
						dag.add_edge(parent,node)
						currentScore = addScore

				else:
					continue

		print(currentScore)
		loopCount += 1

	return(dag)

def compute(infile, outfile):
    # WRITE YOUR CODE HERE
    # FEEL FREE TO CHANGE ANYTHING ANYWHERE IN THE CODE
    # THIS INCLUDES CHANGING THE FUNCTION NAMES, MAKING THE CODE MODULAR, BASICALLY ANYTHING
    
    csvData = pd.read_csv(infile)                      #read in data from .csv file
    idx2names = csvData.columns                        #pandas recognizes first row as column names
    dag = nx.DiGraph()                        #Initialize fully disconnected DAG
    dag.add_nodes_from(range(len(idx2names))) #add nodes

    time.clock()
    finalDag = greedyLocal(csvData,dag,idx2names)
    print(time.clock())

    write_gph(finalDag,idx2names,outfile)

    print(list(nx.simple_cycles(finalDag)))
    pos = nx.shell_layout(finalDag)
    nx.draw_networkx(finalDag,pos=pos,arrows=True,with_labels=True)
    plt.show()
    
    pass


def main():
    if len(inputs) != 2:
        raise Exception("usage: <infile>.csv <outfile>.gph")

    inputfilename = inputs[0]
    outputfilename = inputs[1]
    compute(inputfilename, outputfilename)


if __name__ == '__main__':
    inputs = ["large.csv","large.gph"]
    main()
