#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Grapph object
"""

class Graph():
    """
    The graph object made of nodes, edges and subgraphs 
    """
    def __init__(self):
        self.nodes=[]
        self.edges=[]
        self.subgraphs=[]

    def addNode(self, node):
        """
        Adds a node to the graph
        :param node: Node to add to the graph
        """
        self.nodes.append(node)

    def addEdge(self, edge):
        """
        Adds an edge to the graph
        :param edge: An edge to be added to the graph
        """
        self.nodes.append(edge)

    def addSubgraph(self, subgraph):
        """
        Adds a subgraph to the graph
        :param subgraph: The subgraph to be added 
        """
        self.nodes.append(subgraph)

