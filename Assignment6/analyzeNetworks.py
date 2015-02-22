import sys
import requests
import csv
import pandas as pd
import networkx as nx
import numpy

def readEdgeList(filename):
    edgelist = pd.read_csv(filename)
    if length(edgelist.columns) != 2:
        print "Warning: csv does not contain 2 columns"
        return edgelist.iloc[:, :2]
    return edgelist

def degree(edgeList, in_or_out):
    if in_or_out == 'in':
        return edgeList['1'].value_counts()
    return edgeList['0'].value_counts()

def combineEdgelists(edgeList1, edgeList2):
    return pd.concat(edgeList1, edgeList2).drop_duplicates()

def pandasToNetworkX(edgeList):
    tps = edgeList.to_records(index=False)
    dg = nx.DiGraph()
    dg = dg.add_edges_from(tps)
    return dg

def randomCentralNode(inputDiGraph):
    dg = inputDiGraph
    evc = nx.eigenvector_centrality(dg)
    sm = sum(evc.values())
    nevc = {}
    for key, value in evc.items():
        nevc[key] = value / sm
    randn = numpy.random.choice(nevc.keys(), p=nevc.values())
    return randn
    
