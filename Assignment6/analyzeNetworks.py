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
	df = readEdgeList(edgeList)
	if in_or_out == 'in':
		degree_values = df['artistID_2'].value_counts()
	elif in_or_out == 'out':
		degree_values = df['artist_ID'].value_counts()
	else:
		print("Error")
	return degree_values
#print degree('testcsv.csv', 'in')

def combineEdgelists(edgeList1, edgeList2):
	df1 = readEdgeList(edgeList1)
	df2 = readEdgeList(edgeList2)
	fusion = df1.append(df2)
	fusion.drop_duplicates()
	return fusion
#print combineEdgelists('testcsv.csv', 'testcsv.csv')

def pandasToNetworkx(edgeList):
	graph = nx.DiGraph()
	df = readEdgeList(edgeList)
	edges = df.to_records(index=False)
	graph.add_edges_from(edges)
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