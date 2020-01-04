#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Author: Saifeddine ALOUI
Description:
Grapph object
"""
import enum
from QGraphViz.DotParser.Node import Node

class GraphType(enum.Enum):
    SimpleGraph=0
    DirectedGraph=1        

class Graph(Node):
    """
    The graph object made of nodes, edges and subgraphs 
    """
    def __init__(self, name, graph_type = GraphType.SimpleGraph, parent_graph=None,  **kwargs):
        Node.__init__(self, name, parent_graph, **kwargs)
        self.parent_graph = parent_graph
        self.current_x=0
        self.current_y=0
        self.nodes=[]
        self.edges=[]
        self.graph_type = graph_type

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
   
    def getNodeByName(self, name):
        nodenames = [n.name for n in self.nodes]
        if name in nodenames:
            return self.nodes[nodenames.index(name)]
        else:
            return None

