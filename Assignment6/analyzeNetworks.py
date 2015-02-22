import requests
import pandas as pd
import networkx as nx
import numpy

def readEdgeList(filename):
    edgeList = pd.read_csv(filename)
    if len(edgeList.columns) != 2:
        print "Warning: csv does not contain 2 columns"
        return edgeList.iloc[:, :2]
    return edgeList

def degree(edgeList, in_or_out):
    if in_or_out is 'in':
        return edgeList['1'].value_counts()
    return edgeList['0'].value_counts()

def combineEdgeLists(edgeList1, edgeList2):
    return pd.concat([edgeList1, edgeList2]).drop_duplicates()

def pandasToNetworkX(edgeList):
    tps = edgeList.to_records(index=False)
    dg = nx.DiGraph()
    dg.add_edges_from(tps)
    return dg

def randomCentralNode(inputDiGraph):
    evc = nx.eigenvector_centrality(inputDiGraph)
    sm = sum(evc.values())
    nevc = {}
    for key, value in evc.items():
        nevc[key] = value / sm
    return numpy.random.choice(nevc.keys(), p=nevc.values())
    

