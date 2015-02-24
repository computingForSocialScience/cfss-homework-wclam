import sys
import requests
import pandas as pd
import networkx as nx
import numpy as np

def readEdgeList(filename):
	edgeList = pd.read_csv(filename)
	df = pd.DataFrame(edgeList)
	if len(df.columns) > 2:
		print "Warning: more than two columns. Returning only first two"
		df = df[df.columns[0:2]]
	return df
#print(readEdgeList("testcsv.csv"))

def degree(edgeList, in_or_out):
	if in_or_out is 'in':
		return edgeList['artistID2'].value_counts(sort=True)
	if in_or_out is 'out':
		return edgeList['artistID'].value_counts(sort=True)
	else:
		print("Error")
	
#print degree('testcsv.csv', 'in')

def combineEdgeLists(edgeList1, edgeList2):
	combinedLists = edgeList1.append(edgeList2)
	combinedLists = combinedLists.drop_duplicates()
	return combinedLists 
#print combineEdgelists('testcsv.csv', 'testcsv.csv')

def pandasToNetworkX(edgeList):
	graph = nx.DiGraph()
	for sender,receiver in edgeList.to_records(index=False):
		graph.add_edge(sender,receiver)
	"""df = readEdgeList(edgeList)
	edges = df.to_records(index=False)
	graph.add_edges_from(edges)"""
	#print graph.edges()
	return graph
#print pandasToNetworkx('testcsv.csv')

def randomCentralNode(inputDiGraph):
	edct = nx.eigenvector_centrality(inputDiGraph)
	normal = sum(edct.values())
	for k in edct:
		edct[k] = edct[k]/float(normal)
	randomNode = np.random.choice(edct.keys(), p = edct.values())
	return randomNode

#print randomCentralNode(pandasToNetworkx("testcsv.csv"))